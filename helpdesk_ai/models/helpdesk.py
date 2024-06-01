from odoo import models, api, fields, _
from openai import OpenAI
import json
import time

delimiter = '####'


def save_to_jsonl(data, filename):
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

    # download the file
    with open(filename, 'rb') as f:
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=helpdesk.ticket&field=ai_response&download=true&filename=' + filename,
            'target': 'self',
        }


class CustomHelpdesk(models.Model):
    _inherit = 'helpdesk.ticket'

    ai_response = fields.Text(string='AI Response', readonly=True)

    system_message = fields.Text(string='System Message', compute='_compute_system_message')
    team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team', index=True, tracking=True, required=False)
    def get_tag_ids(self):
        # getting all tags from helpdesk.tag
        tags = self.env['helpdesk.tag'].search([])
        return [(tag.id, tag.name) for tag in tags]

    def get_ticket_types(self):
        # getting all ticket types from helpdesk.ticket.type
        ticket_types = self.env['helpdesk.ticket.type'].search([])
        return [(ticket_type.id, ticket_type.name) for ticket_type in ticket_types]

    def get_teams(self):
        # getting all teams from helpdesk.team
        teams = self.env['helpdesk.team'].search([])
        return [(team.id, team.name) for team in teams]

    def _compute_system_message(self):
        for record in self:
            ticket_types = self.get_ticket_types()
            teams = self.get_teams()

            record.system_message = f"""
            Task: Helpdesk Ticket Classification
            
            Description:
            We need assistance in automatically classifying helpdesk tickets based on their content and context.
            The system should determine the priority level, type (issue or question), and the team to which each ticket should be assigned.
            
            Ticket Details:
            Ticket Name: [Provide the name of the helpdesk ticket here]
            Ticket Description: [Provide the description of the helpdesk ticket here]
            Tags/Categories: [List any relevant tags or categories associated with the ticket]
            Additional Context: [Include any additional context that might be helpful for classification]

            Classification Criteria:
            Priority Levels: 0 (Low Priority), 1 (Medium Priority), 2 (High Priority), 3 (Urgent)
            Ticket Types: {', '.join([ticket_type[1] for ticket_type in ticket_types])}
            Teams: {', '.join([team[1] for team in teams])}
            Tags: {', '.join([tag[1] for tag in self.get_tag_ids()])}

            Expected Response Format:
            - Priority: [Priority level]
            - Type: [Ticket type]
            - Team Assignment: [Assigned team]
            - Tags: [List of related tags]

            Example:
            Ticket Name: "Payroll Calculation Error"
            Ticket Description: "I am unable to calculate the payroll for the month of January."
            Expected Classification:
            - Priority: 2
            - Type: Issue
            - Team Assignment: HR Team
            - Tags: Payroll, HR, Payslip

            Please provide the classification details for the given helpdesk ticket. 
            If you find that the tags that are passed are not relevant, please provide the correct tags according to the 
            description.
            Make sure to provide the correct priority, ticket type, and team assignment based on the description.
            Team Assignment should be one of the following: {', '.join([team[1] for team in teams])}
            Thank you!
            """

    def _compute_ai_response(self, records):
        for record in records:
            description = record.description

            openai_connector = self.env['openai.connector']
            api_key = openai_connector.get_api_key()
            if not api_key:
                raise Exception('API Key not found')

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model='ft:gpt-3.5-turbo-0125:personal::9VIixFo9',
                messages=[
                    {
                        'role': 'system',
                        'content': record.system_message
                    },
                    {
                        'role': 'user',
                        'content': f'Ticket Description: {description} {delimiter} Tags/Categories: {delimiter}'
                                   f' Additional Context: {delimiter}'
                    }
                ],
                temperature=0.0,
            )
            if not response.choices:
                raise Exception('No response from AI')

            ai_response = response.choices[0].message.content
            record.ai_response = ai_response

            ai_response_lines = ai_response.split('\n')
            priority = ai_response_lines[0].split(': ')[1].strip()
            record.priority = priority
            record.ticket_type_id = self.env['helpdesk.ticket.type'].search([('name', '=', ai_response_lines[1]
                                                                              .split(': ')[1].strip())]).id
            tag_names = ai_response_lines[3].split(': ')[1].strip().split(', ')
            tag_ids = []
            for tag in tag_names:
                tag_id = self.env['helpdesk.tag'].search([('name', '=', tag)]).id
                if tag_id:
                    tag_ids.append(tag_id)
                else:
                    tag = self.env['helpdesk.tag'].create({'name': tag})
                    tag_ids.append(tag.id)
            record.tag_ids = [(6, 0, tag_ids)]
            response_team_id = self.env['helpdesk.team'].search([('name', '=', ai_response_lines[2].split(': ')[1]
                                                                  .strip())]).id
            if record.team_id.id == response_team_id:
                record.team_id = response_team_id
            else:
                record.team_id = response_team_id


    @api.model
    def create(self, vals):
        res = super(CustomHelpdesk, self).create(vals)
        self._compute_ai_response(res)
        return res

    def export_tickets_to_jsonl(self):
        today = time.strftime("%Y-%m-%d")
        tickets = self.search([('create_date', '>=', f'{today} 00:00:00'),
                               ('create_date', '<=', f'{today} 23:59:59')])
        data = []
        for ticket in tickets:
            user_content = (
                f"Ticket Description:\n{ticket.description}\n"
                f"Tags/Priority/Helpdesk Team:\n"
                f"- Ticket Name: {ticket.name if ticket.name else 'none'}\n"
                f"- Team: {ticket.team_id.name if ticket.team_id else 'none'}\n"
                f"- Type: {ticket.ticket_type_id.name if ticket.ticket_type_id else 'none'}\n"
                f"- Tags: {', '.join(ticket.tag_ids.mapped('name')) if ticket.tag_ids else 'none'}\n"
                f"- Priority: {ticket.priority if ticket.priority else 'none'}"
            )
            assistant_content = (
                f"Priority: {ticket.priority if ticket.priority else 'none'}\n"
                f"Type: {ticket.ticket_type_id.name if ticket.ticket_type_id else 'none'}\n"
                f"Team Assignment: {ticket.team_id.name if ticket.team_id else 'none'}"
            )
            messages = [
                {"role": "system", "content": "You are a helpful assistant for classifying helpdesk tickets."},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content}
            ]
            data.append({"messages": messages})
        return data

    def fine_tune(self):
        data = self.export_tickets_to_jsonl()
        save_to_jsonl(data, 'tickets_data.jsonl')
