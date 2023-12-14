from django.db import models

class RoleUser(models.Model):
    role = models.CharField(max_length=200, verbose_name='Название роли')

    def __str__(self):
        return f"{self.role}"
class User(models.Model):
    LastName = models.CharField(max_length=50)
    FirstName = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    HashedPassword = models.CharField(max_length=200)
    CreationDate = models.DateTimeField(auto_now=True)
    Role = models.ForeignKey(RoleUser, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"

class Team(models.Model):
    TeamName = models.CharField(max_length=100)
    CreationDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.TeamName
class Role(models.Model):
    role = models.CharField(max_length=200, verbose_name='Название роли')

    def __str__(self):
        return self.role

class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)
    JoinDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.FirstName} {self.user.LastName} in {self.team.TeamName}"

class Task(models.Model):
    Title = models.CharField(max_length=255)
    Description = models.TextField(blank=True)
    Status = models.CharField(max_length=50, default=0)
    Priority = models.IntegerField()
    Start = models.DateTimeField()
    End = models.DateTimeField()
    AssignedUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Title

class TaskContent(models.Model):
    TaskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    Comments = models.TextField(blank=True)
    ChangeHistory = models.TextField(blank=True)
    Attachments = models.TextField(blank=True)

    def __str__(self):
        return f"Content for Task {self.TaskID.Title}"

class Review(models.Model):
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author