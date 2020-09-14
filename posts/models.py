from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from PIL import Image

CATEGORY_CHOICE1 = (
    ('1', 'Art'),
    ('2', 'Buisness'),
    ('3', 'Cooking'),
    ('4', 'Design'),
    ('5', 'Education'),
    ('6', 'Engineering'),
    ('7', 'Entertainment'),
    ('8', 'Food'),
    ('9', 'Goverment'),
)

CATEGORY_CHOICE2 = (
    ('10', 'Healthcare'),
    ('11', 'Languages'),
    ('12', 'Law'),
    ('13', 'Mathematics'),
    ('14', 'Politics'),
    ('15', 'Science'),
    ('16', 'Sports'),
    ('17', 'Technology'),
    ('18', 'Traveling'),
)


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_user')
	title = models.CharField(('Your title...'), max_length=200)
	image = models.ImageField(('Image'), blank=True, default='default.jpg', upload_to='post_images')
	content = models.TextField()
	choice1 = MultiSelectField(('Category'), choices=CATEGORY_CHOICE1, blank=True)
	choice2 = MultiSelectField(('Category'), choices=CATEGORY_CHOICE2, blank=True)
	slug = models.SlugField(unique=True, max_length=50)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('index')

	def save(self, *args, **kwargs):
		self.slug = slugify(str(self.title) + '-by-' + str(self.author))
		super(Post, self).save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 900 or img.width > 900:
			output_size = (900,900)
			img.thumbnail(output_size)
			img.save(self.image.path)


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField(('Comment goes here...'))
	created = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(unique=True, max_length=50, default='None')

	def save(self, *args, **kwargs):
		self.slug = slugify(str(self.content))
		super(Comment, self).save(*args, **kwargs)

	def __str__(self):
		return self.content

	def get_absolute_url(self):
		return reverse('post-detail', args=[self.slug])


class Reply(models.Model):
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField(('Reply goes here...'))

	def get_absolute_url(self):
		return reverse('post-detail', kwargs=[self.slug, self.id])

	def __str__(self):
		return self.content


class Like(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return '{} liked by {}'.format(self.post, self.user)
