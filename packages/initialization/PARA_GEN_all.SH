#!/bin/bash
#############envirenment############
#For AMBER9
source /etc/bashrc
source /yp_home/user/.bashrc
#AMBERHOME=/home/soft/amber9
#PATH=$AMBERHOME/exe:$PATH
#export AMBERHOME PATH
############mol2 file with no total charge
#for mysql
#SQLHOSTNAME="127.0.0.1"
#SQLPORT="3306"
#SQLUSERNAME="root"
#SQLPASSWORD="CCNU@724"
#SQLDBNAME="pfvs_database"
#TABLENAME="acfis_job"
#select_sql="select * from ${TABLENAME}"
#current_id=P$(pwd|cut -c 27-44)
#running_sql="UPDATE  acfis_job SET status='running...' WHERE job_id='${current_id}'"
#error_sql="UPDATE  acfis_job SET status='error!' WHERE job_id='${current_id}'"
#update_sql="UPDATE  acfis_job SET status='finished!' WHERE job_id='${current_id}'"
#email_sql="select mail from acfis_job where job_id='${current_id}'"
#passwd_sql="select password from acfis_job where job_id='${current_id}'"
#queue_sql="SELECT job_id FROM acfis_job where status='queued!' order by id LIMIT 0,1;"
#email=$(mysql -h${SQLHOSTNAME}  -P${SQLPORT}  -u${SQLUSERNAME} -p${SQLPASSWORD} ${SQLDBNAME} -e "${email_sql}"|tail -n +2)
#passwd=$(mysql -h${SQLHOSTNAME}  -P${SQLPORT}  -u${SQLUSERNAME} -p${SQLPASSWORD} ${SQLDBNAME} -e "${passwd_sql}"|tail -n +2)
#echo your job_id is:
#echo $current_id
#echo your email address is:
#echo $email
#echo your passwd:
#echo $passwd
#mysql -h${SQLHOSTNAME}  -P${SQLPORT}  -u${SQLUSERNAME} -p${SQLPASSWORD} ${SQLDBNAME} -e "${running_sql}"
date >>out.log
method=gas
charge=ng
#############pdb file with no total formal charge
if [ $(ls ./cofactor/*.pdb|wc -l) -gt 0 ]
then
cd ./cofactor
for i in *.pdb
do
j=${i%.*}
cp $i ligand2.pdb
echo start PARA_GEN run! >>out.log
echo step1:use babel to convert pdb file to mol2 file and calculate molecule charge!  >>out.log
/yp_home/user/soft/openbabel-2.3.2/bin/babel -ipdb ligand2.pdb -omol2 $j.mol2 -h 
charge=$(printf "%.0f\n" $(sed -n '/@<TRIPOS>ATOM/,/@<TRIPOS>BOND/p' $j.mol2|awk '/ / {sum += $NF};END {print sum}'))
rn=$(sed -n '/@<TRIPOS>ATOM/,/@<TRIPOS>BOND/p' $j.mol2|awk '{print $8}'|sed -n '2,2p'|cut -c 1-3)
echo the residue name of this molecule is:$rn!There may be some problem with your input structure if the residue name is not valid here!  >>out.log
charge_chk1=1
charge_chk2=1
if  [ $charge_chk1 = 1 ] && [ $charge_chk2 = 1 ]
then
echo charge assign by babel:$charge! You may need to asign the total charge manually if charge here is not accurate.>>out.log
else
charge=0
echo WARNING:set total charge to 0, this may not be right! >>out.log
fi
echo step2:use ambertools to generate parameters! >>out.log
echo here is the log of antechamber program: >>out.log
antechamber -i $j.mol2 -fi mol2 -o $i.prep -fo prepi -c $method -nc $charge >>out.log 2>>out.log
echo here is the log of parmchk program: >>out.log
parmchk -i $i.prep -f prepi -o $i.frcmod >/dev/null 2>>out.log
RESN=$(cat *.prep|sed -n "5"p|awk '{print $1}')
sed 's/RESN/'$RESN'/g' leapin >temp
sed 's/NAME/'$i'/g' temp >leapin
rm ligand2*
rm ligand1*
done
cp *.prep *.lib *.frcmod ../
cd ..
fi
##############mol2 file with user-specified charge
if [ -s *.frcmod ]
then
echo prep frcmod file successfully generated! >>out.log
echo step3:use tleap to generate .lib parameters! >>out.log
tleap -f leapin >/dev/null 2>&1
echo job terminated, start to mail the result! >>out.log
zip out.zip *.prep *.frcmod *.lib out.log >/dev/null 2>&1
#rm  /var/www/AUTO_PFVS/result/P$(pwd|cut -c 27-44)/finished.txt
else
echo no frcmod file generated! >>out.log
#touch  /var/www/AUTO_PFVS/result/P$(pwd|cut -c 27-44)/finished.txt
fi
#mysql -h${SQLHOSTNAME}  -P${SQLPORT}  -u${SQLUSERNAME} -p${SQLPASSWORD} ${SQLDBNAME} -e "${update_sql}"
#cp out.zip out.log  /var/www/AUTO_PFVS/result/P$(pwd|cut -c 27-44)
#python sendmail_PARAGEN.py -m 1533892393@qq.com -i out.tar
###########################
