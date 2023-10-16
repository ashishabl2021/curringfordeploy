from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .forms import RegisterUserForm,EditUserForm,TransactionConcretingForm,ProjectForm,SiteForm,ImageUploadForm,StructuralElementForm,ChangePasswordForm
from .models import Curing_Image_Files,Schedule_Curing,Transaction_Concreting,Site_Master,Project_Master,Structural_Element,CustomUser
from datetime import datetime
from datetime import timedelta
from logfile import logdata
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os


def custom_404_view(request, exception=None):
    # You can include any additional context data needed for your template here
    return render(request, 'curingapp/custom_404.html', status=404)

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            messages.info(request,'Login Successful...!')
            return redirect('home')
        else:
            messages.warning(request,'Something went wrong..! please check input ')
            return redirect('loginuser')        
    else:
        return render(request,'curingapp/login.html')

@login_required(login_url="/loginuser/")
def logout_user(request):
    logout(request)
    return redirect("loginuser") 

@login_required(login_url="/loginuser/")
def home(request):
    if request.user.is_authenticated:
        print('Logged')
    else:
        print('not')
    
    variables = { 'page_title': 'Ashoka Buildcon Limited',
                  'username': request.user.get_full_name(), 
                  'isActive' : request.user.is_authenticated,
                  'isSuperUser' : request.user.is_superuser,
                  'app_title':'Document Inbox',
                  'isForm' : True,
                  'isHomePage' : True,
                  'customer_name' : 'Ashoka Buildcon Limited',
                  'isAdmin':request.user.is_Administrator
                }
    return render(request, 'curingapp/home.html', variables)


@login_required(login_url="/loginuser/")
def register_user(request):
    custom_users=CustomUser.objects.all()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            variable = form.save(commit=False)
            variable.save()
            messages.info(request,'Your Account has been Successfully Register...')
            return redirect('register_user')
        else:
            messages.warning(request,'Something went wrong..! Please check form input ')
            return redirect('register_user')

    else:
        form = RegisterUserForm()

    variables = { 'page_title': 'Ashoka Buildcon Limited',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'app_title':'Document Inbox',
                'isForm' : True,
                'isHomePage' : True,
                'form':form,
                'customer_name' : 'Ashoka Buildcon Limited',
                'custom_users':custom_users,
                'isAdmin':request.user.is_Administrator,
            }
    return render(request,'curingapp/register_user.html',variables)

@login_required(login_url="/loginuser/")
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, User_ID=user_id)
    Projects= Project_Master.objects.all()
    Sites= Site_Master.objects.all()
    
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Information Update Successfully')
            return redirect('register_user')  # Redirect to the user list view after editing
    else:
        form = EditUserForm(instance=user)
    variables = { 'page_title': 'Ashoka Buildcon Limited',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isAdmin':request.user.is_Administrator,
                'customer_name' : 'Ashoka Buildcon Limited',
                'app_title':'Document Inbox',
                'isForm' : True,
                'isHomePage' : True,
                'form':form,
                'user': user,
                'Projects':Projects,
                'Sites':Sites,
            }
    return render(request, 'curingapp/edit_user.html', variables)

@login_required(login_url="/loginuser/")
def delete_user(request,user_id):
    if request.user.is_Administrator:  
        user = CustomUser.objects.get(User_ID=user_id)
        user.delete()
        messages.success(request, f"User {user.username} has been deleted.")
        return redirect('register_user')
    else:
        messages.info(request,'Your Not Authorise ')
        return redirect('register_user')

@login_required(login_url="/loginuser/")
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
       
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            msg = "Your password is changed"
            variables = { 'page_title': 'Ashoka Buildcon Limited',
                          'username': request.user.get_full_name(),
                          'isActive' : request.user.is_authenticated,
                          'isSuperUser' : request.user.is_superuser,
                          'isForm' : True,
                          'isHomePage' : True,
                          'customer_name' : 'Ashoka Buildcon Limited',
                          'successalert' : msg,
                          'isAdmin':request.user.is_Administrator,
                        }
            return render(request, 'curingapp/home.html', variables)
        else:
            form = ChangePasswordForm(request.user)
            msg = 'Password do not match or incorrect passwords. Please try again'
            variables = { 'page_title': 'Ashoka Buildcon Limited',
                          'username': request.user.get_full_name(),
                          'isActive' : request.user.is_authenticated,
                          'isSuperUser' : request.user.is_superuser,
                          'isForm' : True,
                          'isHomePage' : True,
                          'customer_name' : 'Ashoka Buildcon Limited',
                          'successalert' : msg,
                          'form' : form,
                          'isAdmin':request.user.is_Administrator,
                        }            
            return render(request, 'curingapp/change_password.html', variables)
    else:
        form = ChangePasswordForm(request.user)
        variables = { 'page_title': 'Ashoka Buildcon Limited',
                      'username': request.user.get_full_name(),
                      'isActive' : request.user.is_authenticated,
                      'isSuperUser' : request.user.is_superuser,
                      'app_title':'Document Inbox',
                      'isForm' : True,
                      'isHomePage' : True,
                      'customer_name' : 'Ashoka Buildcon Limited',
                      'form' : form, 
                      'isAdmin':request.user.is_Administrator,                    
                    }        
        return render(request, 'curingapp/change_password.html', variables)
    
@login_required(login_url="/loginuser/")
def create_project(request):
    projects = Project_Master.objects.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project Added successfully.') 
            return redirect('create_project')  # Redirect to the home page after successful project creation
    else:
        form = ProjectForm()
        variables = { 'page_title': 'Ashoka Buildcon Limited',
                    'username': request.user.get_full_name(), 
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title':'Document Inbox',
                    'isForm' : True,
                    'isHomePage' : True,
                    'customer_name' : 'Ashoka Buildcon Limited',
                    'form': form,
                    'isAdmin':request.user.is_Administrator,
                    'projects':projects,
                }
    return render(request, 'curingapp/create_project.html',variables)

@login_required(login_url="/loginuser/")
def edit_project(request, project_id):
    # Get the project object based on the project_id or return a 404 error if not found
    project = get_object_or_404(Project_Master, Project_ID=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.') 
            return redirect('create_project')  # Redirect to the home page after successful project edit
    else:
        # Create a form instance with the project data
        form = ProjectForm(instance=project)
    
    variables = {
        'page_title': 'Edit Project',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Document Inbox',
        'isForm': True,
        'isHomePage': False,  # Set to False because this is not the home page
        'customer_name': 'Ashoka Buildcon Limited',
        'form': form,
        'project_id': project_id,  # Pass the project_id to the template
        'isAdmin':request.user.is_Administrator,
    }

    return render(request, 'curingapp/edit_project.html', variables)

@login_required(login_url="/loginuser/")
def delete_project(request,project_id):
    if request.user.is_Administrator:
        project = get_object_or_404(Project_Master, Project_ID=project_id)
        project.delete()
        return redirect('create_project')
    else:
        messages.info(request,'Your Not Authorise ')
        return redirect('create_project')

@login_required(login_url="/loginuser/")
def create_site(request):
    sites=Site_Master.objects.all()
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site Added successfully.') 
            return redirect('create_site')  # Redirect to the home page after successful site creation
    else:
        form = SiteForm()
        variables = { 'page_title': 'Ashoka Buildcon Limited',
                  'username': request.user.get_full_name(), 
                  'isActive' : request.user.is_authenticated,
                  'isSuperUser' : request.user.is_superuser,
                  'app_title':'Document Inbox',
                  'isForm' : True,
                  'isHomePage' : True,
                  'customer_name' : 'Ashoka Buildcon Limited',
                  'form': form,
                  'sites':sites,
                  'isAdmin':request.user.is_Administrator,
                }
    return render(request, 'curingapp/create_site.html',variables)


@login_required(login_url="/loginuser/")
def edit_site(request, site_id):
    # Get the site object based on the site_id or return a 404 error if not found
    site = get_object_or_404(Site_Master, Site_ID=site_id)

    if request.method == 'POST':
        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site updated successfully.')          
            return redirect('create_site')  # Redirect to the home page after successful site edit
    else:
        # Create a form instance with the site data
        form = SiteForm(instance=site)

    variables = {
        'page_title': 'Edit Site',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Document Inbox',
        'isForm': True,
        'isHomePage': False,
        'customer_name': 'Ashoka Buildcon Limited',
        'form': form,
        'site_id': site_id,  # Pass the site_id to the template
        'isAdmin':request.user.is_Administrator,
    }

    return render(request, 'curingapp/edit_site.html', variables)

@login_required(login_url="/loginuser/")
def delete_site(request, site_id):
    if request.user.is_Administrator:
        site = get_object_or_404(Site_Master, Site_ID=site_id)
        site.delete()
        messages.success(request, f"{site} has been deleted.")
        return redirect('create_site')
    else:
        messages.info(request,'Your Not Authorise ')
        return redirect('create_site')


@login_required(login_url="/loginuser/")
def create_structural_element(request):
    
    structural_elements=Structural_Element.objects.all()
    if request.method == 'POST':
        form = StructuralElementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Structural Elements Added successfully.') 
            return redirect('create_structural_element')  # Redirect to a success page or another appropriate URL
    else:
        form = StructuralElementForm()
        variables = { 'page_title': 'Ashoka Buildcon Limited',
                  'username': request.user.get_full_name(), 
                  'isActive' : request.user.is_authenticated,
                  'isSuperUser' : request.user.is_superuser,
                  'app_title':'Document Inbox',
                  'isForm' : True,
                  'isHomePage' : True,
                  'customer_name' : 'Ashoka Buildcon Limited',
                  'form': form,
                  'structural_elements':structural_elements,
                  'isAdmin':request.user.is_Administrator,
                }
    return render(request, 'curingapp/create_structural_element.html', variables)

@login_required(login_url="/loginuser/")
def edit_structural_element(request, element_id):
    element = get_object_or_404(Structural_Element, Structural_Element_ID=element_id)
    if request.method == 'POST':
        form = StructuralElementForm(request.POST, instance=element)
        if form.is_valid():
            form.save()
            messages.success(request, 'Structural Element updated successfully.')
            return redirect('create_structural_element')  # Redirect to the home page after successful edit
    else:
        form = StructuralElementForm(instance=element)

    variables = {
        'page_title': 'Edit Structural Element',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Document Inbox',
        'isForm': True,
        'isHomePage': False,
        'customer_name': 'Ashoka Buildcon Limited',
        'form': form,
        'element_id': element_id,
        'isAdmin':request.user.is_Administrator,
    }

    return render(request, 'curingapp/edit_element.html', variables)

@login_required(login_url="/loginuser/")
def delete_structural_element(request, element_id):
    if request.user.is_Administrator:
        element = get_object_or_404(Structural_Element, Structural_Element_ID=element_id)
        element.delete()
        messages.success(request, f"{element} has been deleted.")
        return redirect('create_structural_element')
    else:
        messages.info(request,'Your Not Authorise ')
        return redirect('create_structural_element')

@login_required(login_url="/loginuser/")
def create_schedule_curing(request,user_id):
    user = get_object_or_404(CustomUser, User_ID=user_id)
    

    if request.method == 'POST':
        form = TransactionConcretingForm(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data['Project']
            site_id = form.cleaned_data['Site']
            try:
                # Get the corresponding project and site objects
                project = Project_Master.objects.get(Project_Name=project_id)
                site = Site_Master.objects.get(Site_Name=site_id)
                # Process the form data and save the instance if needed
                transaction_concreting = form.save(commit=False)
                form.instance.User = request.user

                transaction_concreting.Project = project
                transaction_concreting.Site = site
                
                transaction_concreting.save()
                transaction_concreting_id = transaction_concreting.pk  # pk passing for url for see specific schedules for transaction
                # logdata(transaction_concreting)
                
                #selected_structural_element access their data table
                selected_structural_element = transaction_concreting.Structural_Element
                no_of_days = selected_structural_element.No_Of_Days
                frequency=selected_structural_element.Frequency
                time_Bet_TwoCuring=selected_structural_element.Time_Bet_TwoCuring
                # Calculate the initial datetime based on the form submission time
                initial_datetime = datetime.now()
                form.fields['Schedule_Date_and_Time'].initial = initial_datetime
                # Create 10 sets of 2 entries in Schedule_Curing
                

                # Total Hour Count
                # start_time = datetime.strptime('9:30', '%H:%M')
                # end_time = datetime.strptime('6:30', '%H:%M')
                # total_work_hours = (end_time - start_time).seconds / 3600  # Convert seconds to hours


                for i in range(no_of_days):
                    for j in range(frequency):
                        schedule_curing = Schedule_Curing(
                            Transaction_Concreting=transaction_concreting,
                            Project=transaction_concreting.Project,
                            Site=transaction_concreting.Site,
                            Structural_Element=transaction_concreting.Structural_Element,
                            Schedule_Date_and_Time=initial_datetime + timedelta(hours=i * (time_Bet_TwoCuring*2) + j * time_Bet_TwoCuring)
                        )
                        schedule_curing.save()

                return redirect('schedule_curing_table',transaction_concreting_id=transaction_concreting_id)
            except Exception as e: 
                 print(f"Error: {e}")
        else:
            print(form.errors)

    else:
        initial_datetime = datetime.now()
        form = TransactionConcretingForm(initial={'Schedule_Date_and_Time': initial_datetime})
    Projects = Project_Master.objects.all()
    Sites = Site_Master.objects.all()
    
    variables = {
        'page_title': 'Ashoka Buildcon Limited',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Document Inbox',
        'isForm': True,
        'isHomePage': True,
        'customer_name': 'Ashoka Buildcon Limited',
        'form': form,
        'Projects': Projects,
        'Sites': Sites,
        'isAdmin':request.user.is_Administrator,
    }
    return render(request, 'curingapp/start_schedule.html', variables)

@login_required(login_url="/loginuser/")
def get_sites_for_project(request, project_id):
    if request.user.is_Administrator or request.user.is_user:
        # Retrieve the sites for the selected project
        sites = Site_Master.objects.filter(Project_id=project_id)
        # Convert the sites to JSON format
        site_data = [{'id': site.Site_ID, 'name': site.Site_Name} for site in sites]
        return JsonResponse({'sites': site_data})
    else:
        return HttpResponse("You are not Autorized")

@login_required(login_url="/loginuser/")
def schedule_curing_table(request, transaction_concreting_id):
    schedules = Schedule_Curing.objects.filter(Transaction_Concreting_id=transaction_concreting_id)
    transaction = get_object_or_404(Transaction_Concreting, pk=transaction_concreting_id)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            schedule_entry_id = form.cleaned_data['schedule_entry_id']
            schedule_entry = get_object_or_404(Schedule_Curing, pk=schedule_entry_id)

            # Save the uploaded image to the Image_Of_Curing field of the schedule entry
            schedule_entry.Image_Of_Curing = form.cleaned_data['image']
            schedule_entry.save()
            # Redirect back to the same page to prevent resubmission issues
            return redirect('schedule_curing_table', transaction_concreting_id=transaction_concreting_id)
    else:
        form = ImageUploadForm()

    variables = {
        'page_title': 'Ashoka Buildcon Limited',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Document Inbox',
        'isForm': True,
        'isHomePage': True,
        'customer_name': 'Ashoka Buildcon Limited',
        'form': form,
        'transaction': transaction,
        'schedules': schedules,
        'transaction_concreting_id': transaction_concreting_id,
        'isAdmin':request.user.is_Administrator,

    }

    return render(request, 'curingapp/schedule_curing_table.html', variables)

@login_required(login_url="/loginuser/")
def transaction_concreting_list(request):
    transactions = Transaction_Concreting.objects.filter(User=request.user)

    variables = { 'page_title': 'Ashoka Buildcon Limited',
                  'username': request.user.get_full_name(), 
                  'isActive' : request.user.is_authenticated,
                  'isSuperUser' : request.user.is_superuser,
                  'app_title':'Document Inbox',
                  'isForm' : True,
                  'isHomePage' : True,
                  'customer_name' : 'Ashoka Buildcon Limited',
                  'transactions': transactions,
                  'isAdmin':request.user.is_Administrator,
                }
    return render(request, 'curingapp/transaction_concreting_list.html', variables)


@login_required(login_url="/loginuser/")
@csrf_exempt
def upload_image_view(request):
    if request.user.is_user:
        if request.method == 'POST' and request.FILES.get('snap'):
        
            uploaded_image = request.FILES['snap']
            image_path=FileSystemStorage('curingapp/static/curing_images/')
            file=image_path.save(uploaded_image.name,uploaded_image)
            # logdata(file) image save in path 
            
            # Data come from front end
            project_id = request.POST.get("projectID")
            siteID = request.POST.get("siteID")
            transactionID = request.POST.get("transactionID")
            structuralelementID = request.POST.get("structuralelementID")
            scheduleID = request.POST.get("scheduleID")
            # date_and_time = request.POST.get("date_and_time")
            # logdata(project_id)
            # logdata(siteID)
            # logdata(transactionID)
            # logdata(structuralelementID)
            # logdata(scheduleID)
            curing_image_file = Curing_Image_Files(
                Curing_File_Name=uploaded_image.name,
                Project_id=project_id,
                Site_id=siteID,
                Structural_Element_id=structuralelementID,
                Transaction_Concreting_id=transactionID,
                Schedule_Curing_id=scheduleID,
            )
            curing_image_file.save()
            # Save the Curing_Image_Files instance to the database
            return JsonResponse({'message': 'Image uploaded successfully.'})
        else:
            return JsonResponse({'message': 'Image upload failed.'}, status=400)
    else:
        return HttpResponse('You are not autorized')
    
@login_required(login_url="/loginuser/")   
def get_image_list(request):
    if request.user.is_Administrator or request.user.is_user:
        try:
            image_folder = 'curingapp/static/curing_images/'  # Path to your image folder
            image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
            # Return JSON response
            return JsonResponse({'image_files': image_files})
        except Exception as e:
            # Handle exceptions
            return JsonResponse({'error': 'An error occurred'}, status=500)
    else:
        return HttpResponse('You are not autorized')
