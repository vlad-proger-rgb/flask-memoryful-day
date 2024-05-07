# HistoryOfProject.md

History of developing the MemoryfulDay project. I always will try to improve and "expand" it.
The project was started near August of 2023

In the beginning it was on Java Spring Boot.
For the last time it was on Java is was not so pretty. The header had just black links and red when are hovered.
Also the gallery was not implemented and the Search page was working partially.

Then, on January of 2024 I moved it to Python Flask because it was a lot better because in Python I feel myself as if I am writing in regular English (but well, even though it is a programming language, it is still more "Englishy" English)
When I asked ChatGPT to show me a simple example of Flask App, it was amzingly easy. Then, I asked a more complex example.
Since then, I have the back-end on Flask. All the Thymeleaf templates that I had I asked ChatGPT to convert to Jinja templates. And that was pretty fast.

After some time, my brother asked me to write a document about Front-end to complete the task that was given to him from Institute where he was studying. And my project was a good one for this, because it was partially working and the "factual" functionallity is not needed. Only design.

But of course, I like to do some vulnarable coding, so I started to make the project more "completed".
I improved the header as well as the footer blocks.
I repaired the search page because it wasn't working so well. Then, created the DB models by the pattern from the DrawIO that I modelled a lot earlier.

After the document was completed and I sent to brother, I put off the project for some time.

When I met Codeium AI that is COMPLETELY Free, I started to experiment with it.
So, I wanted to somehow try it a real coding. So, I again started to make the project more "completed".
Also, I continued it because I wanted to add MemoryfulAI to the project.
It was the dream of me. A long time ago.
And when I found out LM Studio and local LLMs for free and realized how they are fast and powerful, I started to experiment with it.

I wanted to move my project on GitHub, because all this time I just synced it through Google Drive.
And on GitHub I can see the progress of the project and created some issues.
Before moving on GitHub I wanted to have the project on some "done enough" state. 
So, I started on implementing the Gallery page.
I decided that Gallery will have albums and images in it.
With the help from Codeium AI I implemented albums in less than one day!!!
It is insane!

On 4th and 5th of May I "created" a convienient template for modal windows/fullscreenphoto and started to make it like every UI element has its own functionality in seperate JS file and the modal window is also in seperate file.
So, it is a lot more easier to control. But I still working on it. Now, to add the modal window on some page all I need to do is, well, this: import styles for it, import script for it, put somewhere the {% include 'modal.html' %} and give some button a class name "open-modal__modal-name" and it will work.
And while I doing it, I started to think about React.

So now, 12.08 AM on May 8 of 2024 I completed writing this document. And since now, the project is on GitHub.