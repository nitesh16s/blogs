from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
	author = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	is_male = models.BooleanField(('Male'), default=False)
	is_female = models.BooleanField(('Female'), default=False)
	image = models.ImageField(('Profile Photo'), upload_to='profile_pics')
	background = models.ImageField(('Cover Photo'), upload_to='background', default='default.jpg')
	slug = models.SlugField(unique=True, max_length=50)

	def __str__(self):
		return str(self.author) + ' Profile'

	def get_absolute_url(self):
		return reverse('profile', args=[self.author])

	def save(self):
		self.slug = slugify(str(self.author))
		super(Profile, self).save()

		img = Image.open(self.image.path)
		bac = Image.open(self.background.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

		if bac.height > 1200 or bac.width > 1200:
			output_size = (1200,1200)
			bac.thumbnail(output_size)
			bac.save(self.background.path)



class Connections(models.Model):
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
	following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

	def __str__(self):
		return '{} follows {}'.format(self.follower, self.following)