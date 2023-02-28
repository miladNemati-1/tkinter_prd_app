<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>

<p align="center">
  <img width="460" height="300" src="https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/prd-400.png?raw=true">
</p>

  <h3 align="center">An Automated Polymerization Platform Software</h3>
 
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#Tech-stack">Tech Stack</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

![Welcome_Screen.png](https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/Welcome_Screen.png?raw=true)

This is a desktop application and reaction automation platform created by the Polymer Reaction Design Group at Monash University. It is a program written in python that using certain inputted parameters automates polymerization reactions through pumps and uses analytical instruments such as HNMR and GPC for collecting relevant polymerization data. It features functionalities such as timesweep reactions, database upload for data visualisation, pump control and data cleaning.

The top screenshot shows the homepage of the program, the user chooses the type of reaction they want to run depending on the type of analytical instruments they want to collect data from.

![Timesweeps.png](https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/Timesweeps.png?raw=true)

The user can then choose the time of the reaction they want to run their reaction which then adjusts the flowrates of the pumps accordingly.

![Conversion.png](https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/Conversion.png?raw=true)

The user can then choose how they want their conversions to be calculated based on the conversion screen paramaters and their chosen monomers

![Final.png](https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/Final.png?raw=true)

Finally the user initialises their reaction by giving their reaction a name and following the instructions.

They then press start to start the reaction

![Database.png](https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/Database.png?raw=true)

Once the reaction is finalised the pop ups above will be created which then the user then uploads their data using these screens. This program interacts with a large SQL database to upload its data.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Tech-stack

- Tkinter
- Plotly
- Matplotlib
- HTML
- CSS
- SyringePump
- Numpy
- MySQL
- sqlAlchemy
- regex

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

![Graph_Formula.png](https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/Welcome_Screen.png?raw=true)

The platform interacts with a large chemical database for use in data visualisations of different systems. These visualisations can be customised by the user to generate any combination of data they require and they are able to mathematically modify these graphs.

![Graph_Formula.png](https://github.com/miladNemati-1/django_prd_website/blob/main/images/Graph_Formula.png?raw=true)

![Example_Kinetic_Calc.png](https://github.com/miladNemati-1/django_prd_website/blob/main/images/Example_Kinetic_Calc.png?raw=true)

![All_Rate_Views.png](https://github.com/miladNemati-1/django_prd_website/blob/main/images/All_rate_views.png?raw=true)

The website also dynamically creates descision trees based on data in the database and a set of parameters relating to polymerization reactions. The user can than use these models to get predictions of their next reactions. however the Error is still very high and optimization is needed for future work

![All_Rate_Views.png](https://github.com/miladNemati-1/django_prd_website/blob/main/images/Models_Input.png?raw=true)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

The website also features other administrative tools such as a chemical management system and online lab equipment and chemical search

![Online_Search.png](https://github.com/miladNemati-1/django_prd_website/blob/main/images/Online_Search.png?raw=true)

![My_Lab.png](https://github.com/miladNemati-1/django_prd_website/blob/main/images/My_Lab.png?raw=true)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
## License

Academic license

Polymer Reaction Design Group

https://www.polymatter.net/

<p align="right">(<a href="#readme-top">back to top</a>)</p>
