from django.forms import ModelForm
from .models import Post
from .models import Permissionproject
from django.forms import ModelForm, inlineformset_factory
from django.contrib.auth.models import User

class OrderForm(ModelForm):
	class Meta:
		model = Post
		fields = '__all__'
	
class MemberForm(ModelForm):
    class Meta:
        model = Permissionproject
        exclude = ()

MemberFormSet = inlineformset_factory(Post, Permissionproject,
                                            form=MemberForm, extra=1)


UserFormSet = inlineformset_factory(User, Permissionproject,
                                            form=MemberForm, extra=1)	
