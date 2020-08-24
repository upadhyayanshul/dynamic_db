from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Product
from django.forms import ValidationError
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

class UserForm(UserCreationForm):

    email = forms.EmailField(label="User Email",max_length=150, help_text='* Email is required')
   
    class Meta:
        model = User
        fields = ('username','email', 'password1','password2' )
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = '* Required Alteast 8 Character'
        self.fields['password2'].help_text = '* Required Should Match Password Field'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match,Please Check')
        return password2

class UserProfileForm(forms.ModelForm):
    CHOICES = (('database_1', 'database_1'),
               ('database_2', 'database_2'),
               ('database_3', 'database_3'),
               ('database_4', 'database_4'),
               ('database_5', 'database_5'),)

    address = forms.CharField(required=True,max_length=150,label="User Address", help_text="* Required Field (atlease 5 characters")
    age = forms.IntegerField(required=True,label="Age", help_text="* Digits Accepted")
    database_access = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple(), label="Allow Database Permission",
                                                required=True,help_text="* Required Field (Atleast one selection)")

    class Meta:
        model = Profile
        fields = ('address', 'age', 'database_access')


    def clean_address(self):
       address = self.cleaned_data['address']
       if address and len(address) < 5:
           raise forms.ValidationError("Atleast 5 characters required")
       return address

    def clean_database_access(self):
        database_access = self.cleaned_data['database_access']
        print("database_accessdatabase_accessdatabase_accessdatabase_accessdatabase_access",database_access)
        if not len(database_access):
            raise forms.ValidationError("Please Assign  Atleast One Database")
        return database_access


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','password')
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': '* required field (atlease 8 digits) ',
            'password': '* required field (atlease 8 digits)',
        }

class UserProductForm(forms.ModelForm):
    currencies = (
    ('$', "US Dollars ($)"), 
    )

    title = forms.CharField(max_length=120,required=True,label="Product Title", help_text="* Required field with alpha characters" )
    name = forms.CharField(max_length=40,required=True,label="Product Name", help_text="* Required field max(40) characters" )
    currency = forms.CharField(max_length=5,required=True,label="Currency",help_text="*Required in [US Dollars ($)]")
    price = forms.DecimalField(max_digits=10, decimal_places=2,required=True,label="Price",help_text="* Required with value more than 0")
    sale_price = forms.DecimalField(decimal_places=2, max_digits=10,label="Sales Price",help_text="Optional field (Decimal)")
    active = forms.BooleanField(label="Status",help_text="* Active Product Visible" )
    description = forms.CharField(
        label="Description",required=True ,help_text="*Required short description of product (atlease 50 characters)",
     widget=forms.Textarea(attrs={'placeholder': 'Please enter the  description','rows': 3,
                                  'cols': 100}))


    def __init__(self, *args, **kwargs):
        super(UserProductForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({
                "placeholder": field.label,
                'class': "input-control"
            })

    class Meta:
        model = Product
        fields = ("title", "name", "currency", "price", "sale_price", "active", "description")
       
    def clean_title(self):
        title = to_utf8(self.cleaned_data['title'])
        if (title and not ("".join(title.split(" "))).isalpha()):
            raise forms.ValidationError('Only alpha characters accepted')
        return title

    def clean_description(self):
        description = to_utf8(self.cleaned_data['description'])
        if (description and  len(description)< 50 ):
            raise forms.ValidationError('Need more description of product')
        return description


    def clean(self):
        cleaned_data = super(UserProductForm, self).clean()
        
        active= to_utf8(cleaned_data.get("active",None))

        if(active is None):
            cleaned_data['active']=False
        print("cleaned_data,cleaned_data",cleaned_data)
        return cleaned_data


class DataBaseProductForm(forms.ModelForm):
    CHOICES = (('database_1', 'database_1'),
                   ('database_2', 'database_2'),
                   ('database_3', 'database_3'),
                   ('database_4', 'database_4'),
                   ('database_5', 'database_5'),)

    database_access = forms.ChoiceField(choices=CHOICES, label="Allow Database Permission",
                                               help_text="* Required Field (Atleast one selection)")

    class Meta:
        model = Profile
        fields = ('database_access',)

def to_utf8(d):

    if type(d) is dict:
        return { to_utf8(key):to_utf8(value) for key, value in d.items()}
    elif type(d) is unicode:
        return d.encode('utf8')
    elif type(d) is list:
       return [to_utf8(array) for array in d]
    elif type(d) is tuple:
        return tuple([to_utf8(tuple_data) for tuple_data in d])
    elif type(d) is set:
        return set([to_utf8(set_data) for set_data in tuple(d)])
    elif type(d) is frozenset:
        return frozenset([to_utf8(frozenset_data) for frozenset_data in tuple(d)])
    else:
        return d