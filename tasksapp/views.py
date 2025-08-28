

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Project, Task
from .forms import ProjectForm, TaskForm


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "tasksapp/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "tasksapp/project_form.html"
    success_url = reverse_lazy("project_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "tasksapp/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tasks"] = self.object.tasks.all()
        return ctx


def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("project_detail", pk=project.id)
    else:
        form = TaskForm()
    return render(request, "tasksapp/task_form.html", {"form": form, "project": project})


def task_update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect("project_detail", pk=task.project.id)


