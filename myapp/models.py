from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from random import sample

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profilepics",null=True,blank=True, default="static/images/avatar3.png")
    bio=models.CharField(max_length=200,null=True)
    dob=models.DateTimeField(null=True)
     # symmetrical=false means  user followed person not possible to automatically refollow
    following=models.ManyToManyField("self",related_name="followed_by",symmetrical=False)
    created_date=models.DateTimeField(auto_now_add=True)
    cover_pic=models.ImageField(upload_to="coverpic",blank=True,default="/profilepics/cover.jpg")
    
# profile_obj.following.add(model instance) 
# profile_obj.following.all()
    def __str__(self):
        return self.user.username
    
    @property
    def freind_requests(self):
        all_profiles=UserProfile.objects.all().exclude(user=self.user)
        following_profiles=self.following.all()
        suggestions=set(all_profiles)-set(following_profiles)
        if len(suggestions)>2:
            return sample(list(suggestions),2)
        return suggestions

    def __str__(self) -> str:
        return self.user.username
# profile_obj.following.add(profile_obj)
# profile_obj.following.all()

# post_obj.liked_by.add(model instance) = to like a post with many to many field
# post_obj.liked_by.all()
class Posts(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="postimages",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userposts")
    created_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name="post_like")

    def __str__(self):
        return self.title

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment_text=models.CharField(max_length=200)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="post_comment")
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

#  Django signals
# post_save,pre_save,post_delete,pre_delete

def create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)
