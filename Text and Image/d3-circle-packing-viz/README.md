## README
This is a sample of a D3 visualization you could do with this text analysis data! 

## Getting Started
The tech stack behind this is a bit all over the place, but primarily it's a barebones web app (HTML, CSS, JavaScript) running with a combination of Browserify (so we don't need to press refresh when we make changes) and BeefyJS (a lightweight server to serve up our static files). If you're running this for the first time, you first need to get these dependencies sorted out by running the following in your terminal:

> npm install

Afterwards, you can run the server (and see the visualization) using:

> npm start

This should display a url like, http://127.0.0.1:[port] that you can navigate to on your browser and the app should show up!

## Using the web app
A few notes about the visualization: 
- It's defaulted to use data from samsung.json, but you have the option of importing your own!
    - But it'll only work with the text/image dataset format that you collected from this workshop

Other than that, feel free to click around! The bubbles are colored based on the sentiment value of the article / the average of the related articles. This allows a user to quickly identify articles that have negative (brown) or postive (blue) wording from the headlines. These articles are organized in a hierarchy of related tags where the most frequent tag is given the largest circle. All tags that were used with that larger tag are placed within it's circle. This leads to some duplication, but the idea is that the individual tags are fairly represented. 