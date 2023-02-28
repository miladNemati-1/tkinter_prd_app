<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>

<p align="center">
  <img width="460" height="300" src="https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/prd-400.jpeg?raw=true">
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

![final.png](https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/final.png?raw=true)

Finally the user initialises their reaction by giving their reaction a name and following the instructions.

They then press start to start the reaction

![Database.png](https://github.com/miladNemati-1/tkinter_prd_app/blob/main/images/Database.png?raw=true)

Once the reaction is finalised the pop ups above will be created which then the user then uploads their data using these screens. This program interacts with a large SQL database to upload its data.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Tech-stack

- Tkinter
- Plotly
- Matplotlib
- SyringePump
- Numpy
- MySQL
- sqlAlchemy
- regex

<p align="right">(<a href="#readme-top">back to top</a>)</p>
## License

Academic license

Polymer Reaction Design Group

https://www.polymatter.net/

<p align="right">(<a href="#readme-top">back to top</a>)</p>
