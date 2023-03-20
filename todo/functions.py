from django.http import HttpResponse

from openpyxl import Workbook

def export_to_excel(self, request, *args, **kwargs):
    todos = self.get_queryset()

        
    wb = Workbook()  # Create Workbook
    ws = wb.active

        
 
    ws.append(['ID','Name', 'Description', 'Status', 'Owner', 'Date of Changed'])  # Write Header

       
    for todo in todos:
        owner_user = todo.owner
        username = owner_user.username
        ws.append([todo.id, todo.name, todo.description, todo.status, username, todo.date] )  # Write data to worksheet
            
    file_name = 'todo_export.xlsx'
    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    # Create response object with file attachment
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    # Save workbook to response
    wb.save(response)

    return response