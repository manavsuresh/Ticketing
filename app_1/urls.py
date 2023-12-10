from django.urls import path,include
from . import views
from . import views_login as log
from . import views_ticketing as tick


#For UI output
urlpatterns = [
    path('',log.login,name='login'),
    path('login_check/',log.login_check,name='check'),
    path('index/todo/register/',log.register,name='register'),
    path('index/todo/register/process/',log.process_register,name='process'),
    path('index/todo/register/edit/<str:u_id>',log.edit_register,name='register_edit'),
    path('index/todo/register/edit/done/<str:u_id>',log.edit_register_process,name='register_edit_process'),
    path('index/todo/logout/',log.logout,name='logout'),
    path('index/todo/',tick.todo_,name='to-do'),
    path('index/todo/add/',tick.todo_add,name='to-do_add'),
    path('index/todo/add/addtask/',tick.todo_addtask,name='todo_add'),
    path('index/todo/update/<int:id>',tick.todo_update,name='todo_update'),
    path('index/todo/update/done/<int:id>',tick.todo_mark,name='todo_mark_'),
    path('index/todo/done/<int:id>',tick.todo_mark,name='todo_mark'),
    path('index/todo/update/updatetask/<int:id>',tick.todo_update_task,name='todo_update_task'),
    path('index/todo/remarks/<int:id>',tick.todo_remark,name='todo_update'),
    path('index/todo/remarks/addremarks/<int:id>',tick.todo_remark_task,name='todo_update_task'),
    path('index/todo/filter/',tick.Filter,name='Admin_Filter'),
]