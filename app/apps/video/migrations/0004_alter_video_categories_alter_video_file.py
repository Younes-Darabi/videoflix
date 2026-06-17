from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("video", "0003_remove_video_video_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="category",
            field=models.CharField(
                choices=[
                    ("drama", "Drama"),
                    ("romance", "Romance"),
                    ("action", "Action"),
                    ("comedy", "Comedy"),
                    ("thriller", "Thriller"),
                    ("horror", "Horror"),
                    ("documentary", "Documentary"),
                    ("animation", "Animation"),
                    ("scifi", "Sci-Fi"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="video_file",
            field=models.FileField(upload_to="videos/raw/"),
        ),
    ]
