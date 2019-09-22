
#/usr/bin/bash
now="$(date +'%d-%m-%Y')"
working_dir="$(pwd)"
if [ "$1" == "-h" ]; then
   echo "Kullanım için $0 -f keyword.txt yazmanız gerekmektedir"
   exit 0
fi
if [ "$1" == "" ]; then
   echo "-h yazarak kullanım hakkında bilgi alabilirsiniz"
   exit 1
fi
if [ "$1" == "-f" ]; then

   while IFS= read -r line
   do
       sh -c "./dnsmorph -d $line -json | jq '.results[]|.domain' >> clear.txt"
   done < $2
   exit 0
fi
