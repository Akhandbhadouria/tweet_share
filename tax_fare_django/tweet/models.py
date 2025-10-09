from django.db import models  #provides all the model field types (CharField, TextField, ForeignKey, etc.) and base classes for defining database tables.
from django.contrib.auth.models import User     #importing users from db all the users


class Tweet(models.Model):   #A model in Django represents a database table.
    user=models.ForeignKey(User,on_delete=models.CASCADE) # This creates a foreign key relationship with the User model.
                                                          # Meaning: Each Tweet belongs to one User (but one User can have many tweets).
                                                          # on_delete=models.CASCADE → If a user is deleted, all of their tweets will also be deleted.
    text=models.TextField(max_length=240)
    photo=models.ImageField(upload_to='photo/',
                            blank=True,null=True)
    updated_at =models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user.username}-{self.text[:10]}'

# self.user.username
# Shows the username of the user who posted the tweet.
# Makes it immediately clear who posted the tweet.


# self.text[:10] (but remember, your field is actually test, not text)
# Shows the first 10 characters of the tweet.
# This gives you a quick preview of the tweet without dumping the whole text (which might be long).