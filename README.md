# AILDE
The AILDE is used to optimised a hit compound to lead compounds. The program is written by Python2.7
It includes:
1. The main program ---- AILDE_run_all.py
2. Function package ---- packages
3. parameter file ---- parameter.txt
4. AILDE_RUN  ----- for submitting a job

How to use the program:
1. The requiremnet:
  (1) A GPU linux machine
  (2) the following softwares or librarys should be installed:
      Amber16,Cuda8.0,The Intel(R) MPI Library,JAVA,OpenBabel,ChemAxon,R-3.0(optional)
2. How to setting:
  (1) You should specify the environment variables in the AILDE_RUN (there has been a original version in it, please modify it acoording your machine setting)
  (2) The calculating parameter should be specified in the parameter.txt
      i) steps ---- there are 19 steps in the main program, the 01-18 steps should be run. The 19th step is a optional, that is used to generate a heatmap picture. If you run this step, please install the R-3.0 program
      ii)complex --- the hit-receptor complex PDB file, which you want to optimize
      iii)ligand_name --- the hit compound Residue Name in the complex PDB file, please obtain it from the complex PDB file.
      vi)parallel --- YES or NO, it means whether to use the parallel calculation, if there is multiple GPU and CPU on your machine, you can use YES.
      v)MDstart --- the start step of equilibrium MD simulation, use 3 if you start a new job. If the MD stoped during your calculation, you can modified it to continue the MD calculation
      vi)MDend --- the default is 15, one step means 200ps on the MD simulation, you can set another number bigger than 3.
      vii)mm_pbsa ---- it specified the location of parameter file for calculating MMPBSA. Just use the default value if the package directory is at the same location with parameter.txt.
      viii)md_request --- it specified whether you want to add a subsequent short MD simulation on the newly obtained lead compound, default is NO.
      viiii)entropy --- it specified the location of parameter file for calculating entropy change. Just use the default value if the package directory is at the same location with parameter.txt. 

   the parameter you need to modify is just i),ii) and iii). Others can use default value.
   You can also see our web version for reference at http://chemyang.ccnu.edu.cn/ccb/server/AILDE/
