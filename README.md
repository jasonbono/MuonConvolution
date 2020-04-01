# MuonConvolution


We have particles called muons moving through a magnetic field. The field changes with location and time. The muons' trajectories are complex. **We want to know the average magnetic field experienced by the muons.** 

(An analogy is finding the average water temperature experienced by a school of :fish: as they swim  through various depths and currents, and throughout the day.)

### How: A (very) simplified explanation
Ultimately, we get 2D projections of the muon distribution, eg:
![image](https://drive.google.com/uc?export=view&id=174tx8yv8ITmqFdtiiO3TUytxuUOKJIFe)

And 2D projections of the magnetic field, eg:
![image](https://drive.google.com/uc?export=view&id=1ZCSGLTyMzHMvvA7AZktWK0XT2pD5XG3O)

And we take the element-wise product of the two distributions above to get a geometric representation of where contributions to the averaged field are coming from, as shown below:
![image](https://drive.google.com/uc?export=view&id=1U3g-nt_A_yrLvpwta9AB_yEA0DqWuBzw)
We integrate the distribution above to get the average field experienced by the muons!

### Why
We can combine the average magnetic field with information on how the muons behave in that magnetic field to help answer basic questions about how all matter behaves! 


## Getting Started
These instructions will help get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

- python 3
- jupyter (tested on version 5.7.8)
- numpy (tested on version 1.17.0)
- pandas (tested on version 0.25.0)
- psycopg2 (tested on version 2.8.2)
- optional : pyroot (for reading of ROOT data in python. Alternatively, you can reformat ROOT data via C++)
- optional: matplotlib

Some of the required data is in the gm2 online database. To manually browse the database via terminal, try:

	psql -U gm2_reader -d gm2_online_prod -h localhost -p 5434



### Contributing

1. Fork it (<https://github.com/jasonbono/MuonConvolution/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


### Your first task: tutorials!

The foundation of this analysis is the "grid" and "moments" methods. If you can run and understand the notebooks `~/grid_tutorial.ipynb` and `~/moments_tutorial.ipynb`, and understand the libs that they use, then you should be able to develop freely from there

### A suggested second task: muon position error evaluation

Now that you get the basics, check out `~/analysis/systematics/beam_motion.ipynb` to see a foundational method for evaluating systematic uncertainty.

Similarly, see `~/analysis/systematics/close_orbit_distortions.ipynb` to see how closed orbit distortions are handeled.

### A suggested third task: statistical and field error propegation

There is no one correct way to propegate field error for this project. To see my approach, check out `/analysis/run1_pipeline/analyze_all_runs.ipynb`

Also, check out my incomplete note at `background/calculation/calculation.pdf` for some ideas. *Warning* Some of the note has false reasoning and incorrect conclusions!



## Authors

* **Jason Bono** - *Initial work* - [JasonBono](https://github.com/JasonBono)

 

	






