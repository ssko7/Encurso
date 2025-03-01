from django.db import models

class User(models.Model):
    encurso_id = models.CharField(max_length=255, unique=True,null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    dob = models.CharField(max_length=10, blank=True, null=True)
    home_town = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    institute = models.CharField(max_length=255, blank=True, null=True)
    institute_place = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(max_length=255, blank=True, null=True)
    has_paid_basicfee = models.BooleanField(default=False)
    workshop = models.CharField(max_length=255, blank=True, null=True)
    event = models.CharField(max_length=255, blank=True, null=True)
    accommodation = models.BooleanField(default=False)
    food = models.BooleanField(default=False)
    workshop_total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    event_total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    workshop_payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    event_payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    workshop_razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    workshop_razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    workshop_razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    event_razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    event_razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    event_razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.full_name

class Workshop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    requires_team = models.BooleanField(default=False)
    content = models.TextField(default="")
    timing = models.CharField(max_length=255, blank=True, null=True)
    instructor = models.CharField(max_length=255, blank=True, null=True) 
    layout=models.CharField(max_length=50,choices=[('evlayout','EV Layout'),
                                                   ('iotlayout','IoT Layout'),
                                                   ('matlablayout','MATLAB Layout'),
                                                   ('dronelayout','Drone Layout'),
                                                   ],null=True,blank=True)

    def __str__(self):
        return self.name

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    team_name = models.CharField(max_length=255, blank=True, null=True)  # Only for team-based workshops
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.full_name} - {self.workshop.name}"

class TeamMember(models.Model):
    members = models.CharField(max_length=255, blank=True, null=True)
    workshop = models.CharField(max_length=255, blank=True, null=True)
    event = models.CharField(max_length=255, blank=True, null=True)

class Events(models.Model):
    name = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    requires_team = models.BooleanField(default=False)
    max_team_size = models.PositiveIntegerField(default=1)
    timing = models.DateTimeField(null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    layout=models.CharField(max_length=50,choices=[('cktlayout','Ckt Layout'),
                                                   ('pplayout','PP Layout'),
                                                   ('hackathonlayout','Hachathon Layout'),
                                                   ('quizzlayout','Quizz Layout'),
                                                   ('projectlayout','Project Layout'),
                                                   ('photolayout','Photo Layout'),
                                                   ],null=True,blank=True)
    def __str__(self):
        return self.name

class Sponsor(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Sponsoring brand name
    logo = models.ImageField(upload_to='sponsors/', blank=True, null=True)  # Sponsor logo

    def str(self):
        return f'{ self.name}-{self.logo}'
    
class workshop_members(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    encurso_id = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    home_town = models.CharField(max_length=255, blank=True, null=True)
    institute = models.CharField(max_length=255, blank=True, null=True)
    workshop = models.CharField(max_length=255, blank=True,null= True)

class event_members(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    encurso_id = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    home_town = models.CharField(max_length=255, blank=True, null=True)
    institute = models.CharField(max_length=255, blank=True, null=True)
    workshop = models.CharField(max_length=255, blank=True,null= True)
