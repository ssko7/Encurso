from django.urls import path
from .views import  contactus,refund,privacy,terms,verify_encurso_id,verify_payment_workshop,register_workshop,index,basic_fee_payment,basic_payment_page,verify_payment_event,register_event,home,dronelayout_view,evlayout_view,iotlayout_view,matlablayout_view,cktlayout_view,hackathonlayout_view,pplayout_view,quizzlayout_view,photolayout_view,projectlayout_view,workshop_detail,event_detail,verify_payment,create_encurso_id



urlpatterns = [
    path('contact.html/',contactus,name='contactus'),

    path('refund.html/',refund,name='refund'),
    path('privacy.html/', privacy, name='privacy'),
    path('terms.html/',terms,name='terms'),
    path('register_workshop/terms.html',terms,name='terms'),
    path('register_event/terms.html',terms,name='terms'),
    path('terms/',terms,name='terms'),
    path('basicpayment/terms/',terms,name='terms'),
    path('create_encurso_id/', create_encurso_id, name='create_encurso_id'),
    path('verify_payment_workshop/', verify_payment_workshop, name='verify_payment_workshop'),
    path('verify_encurso_id/', verify_encurso_id, name='verify_encurso_id'),
    path('verify_payment_workshop/', verify_payment_workshop, name='verify_payment_workshop'),
    path('verify_payment_event/', verify_payment_event, name='verify_payment_event'),
    path('register_event/', register_event, name='register_event'),
    path('basicfee/', basic_fee_payment, name='basic_fee_payment'),
    path('basicpayment/', basic_payment_page, name='basic_payment_page'),
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('register_workshop/', register_workshop, name='register_workshop'),
    path('i/',index,name='index'),
    path('',home,name='home'),
    path('drone/',dronelayout_view,name='drone'),
    path('ev/',evlayout_view,name='ev'),
    path('iot/',iotlayout_view,name='iot'),
    path('matlab/',matlablayout_view,name='matlab'),
    path('ckt/',cktlayout_view,name='ckt'),
    path('hackathon/',hackathonlayout_view,name='hackathon'),
    path('pp/',pplayout_view,name='pp'),
    path('quizz/',quizzlayout_view,name='quizz'),
    path('photo/',photolayout_view,name='photo'),
     path('workshops/ev/', evlayout_view, name='evlayout_view'),
    path('workshops/drone/', dronelayout_view, name='dronelayout_view'),
    path('workshops/iot/', iotlayout_view, name='iotlayout_view'),
    path('workshops/matlab/', matlablayout_view, name='matlablayout_view'),
    path('project/',projectlayout_view,name='project'),
    
    path('events/pp/', pplayout_view, name='pplayout_view'),
    path('events/quizz/', quizzlayout_view, name='quizzlayout_view'),
    path('events/hackathon/', hackathonlayout_view, name='hackathonlayout_view'),
    path('events/ckt/', cktlayout_view, name='cktlayout_view'),
    path('events/photolayout/', photolayout_view, name='photolayout_view'),
    path('events/project/', projectlayout_view, name='projectlayout_view'),
    path('project/',projectlayout_view,name='project'),
    path('workshops/<int:workshop_id>/', workshop_detail, name='workshop_detail'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),

]
