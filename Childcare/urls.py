
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path
from Child.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home,name='home'),
    path('discussion/<str:pk>/', discussion, name="discussion"),
    path('discussion_topic', discussion_topicpage, name="discussion_topicpage"),
    path('discussion_form/', createDiscussion, name="createDiscussion"),
    path('update-discussion/<str:pk>/', updateDiscussion, name="updateDiscussion"),
    path('delete-discussion/<str:pk>/', deleteDiscussion, name="deleteDiscussion"),
    path('delete-message/<str:pk>/', deleteMessage, name="deleteMessage"),
    path("update_order/<str:pk>/",updateOrder,name='updateOrder'),
    path("delete/<str:pk>/",deleteOrder,name='deleteOrder'),
    path("order1_form/<str:pk>",createOrder,name='createOrder'),
    path("product",productpage,name='productpage'),
    path("orderedlist",orderedpage,name='orderedpage'),
    path("feature",featurepage,name='featurepage'),
    path("about",aboutpage,name='aboutpage'),
    path("video",videopage,name='videopage'),
    path("payment",paymentpage,name='paymentpage'),
    path("bkash",bkashpage,name='bkashpage'),
    path("nagad",Nagadpage,name='nagadpage'),
    path("help",helppage,name='helppage'),
    path("update_help/<str:pk>/",updatehelp,name='updatehelp'),
    path("delete_help/<str:pk>/",deleteHelp,name='deleteHelp'),
    path("delete_comment/<str:pk>/",deleteComments,name='deleteComments'),
    path("adminpage",adminpage,name='adminpage'),
    path("contact",contactpage,name='contactpage'),
    path("daycare",daycare,name='daycare'),
    path("profile",profilepage,name='profilepage'),
    path('signup', handleSignUp, name="handleSignUp"),
    path('login', handeLogin, name="handleLogin"),
    path('logout', handelLogout, name="handleLogout"),
    path('school', addschool, name="addschool"),
    path('<int:pk>/', schoolupdate, name='ambuupdate'),
    path('ajax/load-schools/', load_schools, name='ajax_load_schools'), # AJAX
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

