from django.shortcuts import render

def student_info(request):
    """
    Display student information
    """
    # Hardcoded student data (not from database as requested)
    student_data = {
        'student_name': 'Prince Raj Kiran',
        'roll_number': '2403051050507',
        'branch': 'Computer Science & Engineering',
        'semester': '4th'
    }
    
    return render(request, 'hello/student_info.html', {'student_data': student_data})
