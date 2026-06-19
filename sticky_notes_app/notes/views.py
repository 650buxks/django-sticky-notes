from django.shortcuts import render, redirect, get_object_or_404
from .models import StickyNote


def index(request):
    # Check if the user is submitting the form
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Save the new note directly to SQLite
        StickyNote.objects.create(title=title, content=content)

        # Refresh the page to show the new note
        return redirect('index')

    # If it's just a regular page load (GET), display the notes
    notes = StickyNote.objects.all().order_by('-created_at')
    return render(request, 'notes/index.html', {'notes': notes})


def delete_note(request, note_id):
    note = get_object_or_404(StickyNote, id=note_id)
    note.delete()
    return redirect('index')


def edit_note(request, note_id):
    note = get_object_or_404(StickyNote, id=note_id)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        return redirect('index')
    return render(request, 'notes/edit.html', {'note': note})
