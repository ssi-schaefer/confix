#!/bin/sh

ECHO="echo -e "  # \ sequences (\n, ...) are interpreted
export PATH="/usr/local/bin:$PATH"

# Usage-Subroutine
usage()
{
  $ECHO '\n'
  $ECHO '  usage: $0 [-h] [-clean] [-clobber] [-make] [-upd] [-noi] '
  $ECHO '           [-uninst] [-confClean] ["-m module1 -m modul2 ..."]'
  $ECHO '\n'
  $ECHO '    Without any options given performs:'
  $ECHO '      confix.py --boo --configure --make --targets=install'
  $ECHO '    in all modules given in your $HOME/.envMakeModule file'
  $ECHO '      -h            ... this help'
  $ECHO '      -clean        ... removes contents build dir'
  $ECHO '      -clobber      ... removes package dir and then performs clean'
  $ECHO '      -make         ... performs only make in build dir'
  $ECHO '      -upd          ... performs first cvs update -d -P'
  $ECHO '      -noi          ... don`t perform install'
  $ECHO '      -uninst       ... perform uninstall'
  $ECHO '      -confClean    ... removes all autoconf and automake generated files'
  $ECHO '      -m moduleName ... only performs the given module(s)'
  exit 1
}

#make -j 2 - ... equiv. in confix: --target="-j 2 -..."
# make with 1 CPU
#defaultInst='--targets=""'
# make with 2 CPU's
defaultInst='--targets="-j 2 "'

# sourcing envFile
envFile="$HOME/.envMakeModule"
if [ ! -f $envFile ]
then
  $ECHO "\n$envFile does not exist\n"
  exit 1
fi

. $envFile

clean=0
clobber=0
make=0
moduleList=""
install="install"
confCleaning=0
confCleanList=".aclocal.m4.swp aclocal.m4 Makefile.am Makefile.in depcomp config* stamp-h.in missing mkinstalldirs"
update=0

cnt=0
for arg
do
  case $arg in 
      -make)  make=1;
              shift;
              ;;
#      -m)     shift;
#              moduleList="$moduleList $1";shift;
#              ;;
      -m)     shift;
              cnt=0;
              for li in $allModulesList
              do
                echo "Param:$li"
                case $li in
                  $1*) cnt=`expr $cnt + 1`;
                       param="$li";echo Match:$param;;
                esac
              done
              if [ $cnt -ne 1 ]
              then
                moduleList="$moduleList $1";
              else
                moduleList="$moduleList $param";
              fi
              shift;
              ;;
      -clean) clean=1; 
              shift;
              ;;
      -clobber) clean=1;clobber=1 
              shift;
              ;;
      -noi) install="";
              shift;
              ;;
      -uninst) install="uninstall";
              shift;
              ;;
      -confClean) confCleaning=1;
              shift;
              ;;
      -upd) update=1;
              shift;
              ;;
      -*)      usage;
               exit;;
  esac
done

if [ $clobber -eq 1 ]
then
  $ECHO "\nMaking clobber ..."
  $ECHO "\nRemoving $packageDir ..."
  rm -rf "$packageDir"/*
fi

if [ "$moduleList" = "" ]
then
  if [ "$defaultModuleList" = "" ]
  then
    $ECHO "\nNo modules to be done ... \n"
  else
    moduleList=$defaultModuleList
  fi

fi

$ECHO "\nBootstrapping and make $install for $moduleList ...\n"

for module in $moduleList
do
  moduleBuildDir=$buildDir"/"$module
  moduleSourceDir=$sourceDir"/"$module
  if [ ! -d $moduleBuildDir ] 
  then
    $ECHO "\n$moduleBuildDir does not exist ... exiting \n"
    exit 1
  fi
  if [ $clean -eq 1 ]
  then
    $ECHO "\nMaking clean"
    $ECHO "Removing $moduleBuildDir ...\n"
    rm -rf "$moduleBuildDir"/*
  fi

  $ECHO "\n ==>Bootstrapping,configuring, ... in $moduleSourceDir ...\n"
  cd $moduleSourceDir
  if [ $confCleaning -eq 1 ]
  then
    $ECHO "\nCleaning up conf generated files ...\n"
    rm $confCleanList
  fi
  if [ $update -eq 1 ]
  then
    $ECHO "\nUpdating $moduleSourceDir ... \n"
    cvs update -d -P
  fi
  if [ $make -eq 1 ]
  then
    eval confix.py --make $defaultInst$install
  else
    eval confix.py --boo --configure --make $defaultInst$install 
  fi
  echo "Exit value = $?"
done




