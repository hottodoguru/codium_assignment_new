from openpyxl import Workbook


def export_to_excel(self, request, *args, **kwargs):
    todos = self.get_queryset()

    wb = Workbook()  # Create Workbook
    ws = wb.active

    ws.append(['ID', 'Name', 'Description', 'Status', 'Owner', 'Date of Changed'])  # Write Header

    for todo in todos:
        owner_user = todo.owner
        username = owner_user.username
        ws.append([todo.id, todo.name, todo.description, todo.status, username, todo.date])  # Write data to worksheet

    return wb
