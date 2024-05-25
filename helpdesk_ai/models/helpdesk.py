from odoo import models, api, fields, _
from openai import OpenAI

delimiter = '####'

class CustomHelpdesk(models.Model):
    _inherit = 'helpdesk.ticket'

    ai_response = fields.Text(string='AI Response', readonly=True)

    system_message = fields.Text(string='System Message', compute='_compute_system_message')

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
            Ticket Description: [Provide the description of the helpdesk ticket here]
            Tags/Categories: [List any relevant tags or categories associated with the ticket]
            Additional Context: [Include any additional context that might be helpful for classification]

            Classification Criteria:
            Priority Levels: 0 (Low Priority), 1 (Medium Priority), 2 (High Priority), 3 (Urgent)
            Ticket Types: {', '.join([ticket_type[1] for ticket_type in ticket_types])}
            Teams: {self.team_id.name if self.team_id else ', '.join([team[1] for team in teams])}
            Tags: {', '.join([tag[1] for tag in self.get_tag_ids()])}

            Expected Response Format:
            - Priority: [Priority level]
            - Type: [Ticket type]
            - Team Assignment: [Assigned team]
            - Tags: [List of related tags]

            Example:
            Ticket Description: "I am experiencing issues with accessing my account."
            Expected Classification:
            - Priority: 2
            - Type: Issue
            - Team Assignment: Support
            - Tags: Account Access, Technical Issues

            Please provide the classification details for the given helpdesk ticket. 
            If you find that the tags that are passed are not relevant, please provide the correct tags according to the 
            description.
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
                model='gpt-4',
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
            response_time_id = self.env['helpdesk.team'].search([('name', '=', ai_response_lines[2].split(': ')[1]
                                                                  .strip())]).id
            if record.team_id.id == response_time_id:
                record.team_id = response_time_id

    @api.model
    def create(self, vals):
        res = super(CustomHelpdesk, self).create(vals)
        self._compute_ai_response(res)
        return res
