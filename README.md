# samferda
A Python script powered by Selenium to filter rides on the Icelandic car-pooling website samferda.net

 ## Introduction
 I'm about to go for a month-long roadtrip on Iceland.
 Planning the trip, I realized that unfortunatley, Iceland doesn't have railroads, and the public bus service only covers parts of the ring-road, Iceland's main highway that goes all around the island.
 This makes the use of car pretty much mandatory to explore <b> "The land of fire and ice" </b>. To solve this issue, Icelanders created a beautiful website called http://samferda.net that helps people to find travel partners to share the ride with. 
 As they say on their website, <i>Iceland has more car than people, therefore you can always find someone who's going in the same place as you.</i>
 This makes travel cheaper and better for the environment.

 Nevertheless, samferda doesn't have a filter function on their website, so finding travel partners can take a lot of time as you'd need to check each ride request individually on the website.
 Therefore, I created a simple Python that helps you find only the results that match your filtering criteria.

 As an output, the script gives you a <b>.csv</b> file with the contact informations of only the travel partners that suit your needs!
 
 ## Setting up the script
 The script uses Selenium to scrape data from samferda website using Google Chrome WebDriver.
 
 A WebDriver is a browser automation framework that makes the script talk with a web browser's APIs. For this project, we simply need to access to the HTML page of each ride.
 You can find its Google Chrome ChromeDriver, at this link: https://chromedriver.chromium.org

 Once you've downloaded it, you can move the file to a known location and assign its position to the variable <b>CHROME_DRIVER_PATH</b> on the first lines of the script.

 You can also specify the output .csv file name and path by modifying the value of the variable <b>OUTPUT_FILE</b>.

 Lastly, you can also edit the number of thread used by the script by adding the argument thread to the function that invokes the ThreadPoolExecutor. The default value for <i>threads</i> parameter is 7.
  ```
 run_onthreads(rides)
 ```
 For instance, should you like to use 10 threads you can edit the line as follows:
 ```
 run_onthreads(rides, threads=10)
 ```
 ## How to define filters
 You just need to run <b> main.py </b> and it will ask you the details to filter the result.
 First, type P if you would like to find people to carry with your car, or R if you would like to join someone else's car:
  ```
    Would you like to join someone else's ride [R] or to find people to join your ride? [P]: R
 ```
 Insert the starting date, as shown:
 ```
    Please insert your desidered start date [yyyy-mm-dd]: 2022-08-10
 ```
 Then, insert the last date:
 ```
    Please insert your desidered end date [yyyy-mm-dd]: 2022-08-20
 ```
 Lastly, insert the number of passengers:
 ```
    Please insert your desidered number of passengers: 2
 ```

 The script will start the scraping process, and the result will look something like this:
 ```
 Requesting: Passengers
 origin: Mývatn
 destination: Vík
 date: 2022-8-12
 time: 07:00
 seats: 2
 name: Marielle
 phone: xxxxxxxx
 mail: xxx@yyy.com
 comment: We are looking for 2 passengers without luggage or 1 with luggage, to split the cost of the rental car (265€) and the fuel. If the time above doesn't work, we can arrange the ride to be in the next morning from Keflavik or Reykjavik.

============= ---- -- ---- =============

requesting: Passengers
origin: Reykjaví­k
destination: Vík
date: 2022-8-15
time: 10:00
seats: 2
name: Fani
phone: xxxxxxxx
mail: xxx@yyy.com
comment: We are looking for 2 passengers without luggage or 1 with luggage, to split the cost of the rental car (265€) and the fuel. If the time above doesn't work, we can arrange the ride to be later in the day from Grindavik, Keflavik or Reykjavik.

============= ---- -- ---- =============
...

```

The .csv with the rides details will also be generated and saved in the specified path defined at <b>OUTPUT_FILE</b>.