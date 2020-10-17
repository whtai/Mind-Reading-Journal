import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone

from .sentiment import analyze_sentiment

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    senti_score = models.FloatField(blank=True, null=True)
    senti_magnitude = models.FloatField(blank=True, null=True)

    def classify_sentiment(self):
        if self.senti_score is None or self.senti_magnitude is None:
            self.calculate_sentiment_score()

        if self.senti_score > 0.15 :
            return 'Positive'
        elif self.senti_score < -0.15 :
            return 'Negative'
        elif self.senti_magnitude < 0.1 :
            return 'Neutral'
        else:
            return 'Mixed'

    def calculate_sentiment_score(self):
        self.senti_score, self.senti_magnitude = analyze_sentiment(self.text)
        self.save()
        
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
