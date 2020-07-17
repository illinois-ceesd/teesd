import sys
import os
import platform
import stat
import teesd


def generate_suite_runner(suitename, suitepath, outputpath):

    programname = "generate_serial_suite_runner"

    nodename = platform.node()
    #    systemName = platform.system()
    systemtype = "workstation"

    systemid = nodename.find("quartz")
    if systemid >= 0:
        systemtype = "quartz"

    systemid = nodename.find("lassen")
    if systemid >= 0:
        systemtype = "lassen"

    scriptshortname = "serial_" + suitename
    scriptname = scriptshortname + ".sh"
    scriptfilename = outputpath + "/" + scriptname
    spawnername = scriptshortname + "_spawner.sh"
    spawnerpath = outputpath + "/" + spawnername
    resultsfilename = outputpath + "/serial_" + suitename + "_results.txt"
    testlistfile = suitepath + "/testlist.txt"
    teesdpath = teesd.teesdpath
#    teesdsourcepath = teesd.sourcepath
#    teesdbinpath = teesd.binpath

    #    testNames = open(testlistfile).readlines()
    #    numTests = len(testNames)
    #    print(programname,": SuiteName = ",suitename)
    #    print(programname,": SuitePath = ",suitepath)
    #    print(programname,": OutPath   = ",outputpath)
    #    print(programname,": Machine   = ",platform.machine())
    #    print(programname,": Node      = ",platform.node())
    #    print(programname,": Platform  = ",platform.platform())
    #    print(programname,": Processor = ",platform.processor())
    #    print(programname,": System    = ",platform.system())
    #    print(programname,": UName     = ",platform.uname())

    print(programname+": Generating script for suite(", suitename, ")")
    print(programname+": System Type(", systemtype, ")")
    print(programname+": scriptfilename  = ", scriptfilename)
    print(programname+": resultsfilename = ", resultsfilename)

    if systemtype == "workstation":
        print(programname+": Generating for user workstation.")
        # Then it's an mpiexec situation
        outscript = open(scriptfilename, "w")
        print("#!/bin/sh\n\n", file=outscript)
        print("export PYOPENCL_CTX=''", file=outscript)
        print(
            'export PYTHONPATH="' + teesdpath + ':${PYTHONPATH}"',
            file=outscript,
        )
        print("rm -f ", resultsfilename, file=outscript)
        print("for testname in $(cat ", testlistfile, ")\n", file=outscript)
        print("do\n", file=outscript)
        print(
            '     printf "',
            scriptshortname,
            ": Running test",
            ' (${testname})...\\n"',
            file=outscript,
        )
        print(
            '     printf "',
            scriptshortname,
            ": Command: ",
            " python ",
            suitepath + "/${testname}.py ",
            resultsfilename,
            '\\n"\n',
            file=outscript,
        )
        print("     date\n", file=outscript)
        print(
            "     python ",
            suitepath + "/${testname}.py ",
            resultsfilename,
            "\n",
            file=outscript,
        )
        print("     date\n", file=outscript)
        print("done\n", file=outscript)
        outscript.close()
        os.chmod(scriptfilename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    if systemtype == "quartz":
        print(programname+": Generating for Quartz@LLNL.")
        # We need to generate a suite runner that runs a parallel
        # spawning script. First; the spawning script:
        outscript = open(spawnerpath, "w")
        print("#!/bin/sh\n\n", file=outscript)
        print("export PYOPENCL_CTX=':'", file=outscript)
        print(
            'export PYTHONPATH="' + teesdpath + ':${PYTHONPATH}"',
            file=outscript,
        )
        print("rm -f ", resultsfilename, file=outscript)
        print("for testname in $(cat ", testlistfile, ")\n", file=outscript)
        print("do\n", file=outscript)
        print(
            '     printf "',
            scriptshortname,
            ": Running test",
            ' (${testname})...\\n"',
            file=outscript,
        )
        print(
            '     printf "',
            scriptshortname,
            ": Command: ",
            " srun -n 1 python ",
            suitepath + "/${testname}.py ",
            resultsfilename,
            '\\n"\n',
            file=outscript,
        )
        print("     date\n", file=outscript)
        print(
            " srun -n 1 python ",
            suitepath + "/${testname}.py ",
            resultsfilename,
            "\n",
            file=outscript,
        )
        print("     date\n", file=outscript)
        print("done\n", file=outscript)
        outscript.close()
        os.chmod(spawnerpath, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        # Now the suite runner:
        outscript = open(scriptfilename, "w")
        numnodes = 1
        numprocjob = 1
#        numproctest = 1
        timeout = 10
        # print("#!/bin/bash\n\nset -x\ndate", file=outscript)
        print("#!/bin/bash\n\ndate", file=outscript)
        print(
            "salloc -N "
            + str(numnodes)
            + " -n "
            + str(numprocjob)
            + " -t "
            + str(timeout)
            + " -ppdebug "
            + spawnerpath,
            file=outscript,
        )
        print("errorCode=$?", file=outscript)
        print("date", file=outscript)
        print("exit $errorCode", file=outscript)
        outscript.close()
        os.chmod(scriptfilename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    if systemtype == "lassen":
        print(programname+": Generating for Lassen@LLNL.")
        # We need to generate a suite runner that runs a parallel
        # spawning script. First; the spawning script:
        outscript = open(spawnerpath, "w")
        print("#!/bin/sh\n\n", file=outscript)
        print("export PYOPENCL_CTX=''", file=outscript)
        print(
            'export PYTHONPATH="' + teesdpath + ':${PYTHONPATH}"',
            file=outscript,
        )
        print("rm -f ", resultsfilename, file=outscript)
        print("for testname in $(cat ", testlistfile, ")\n", file=outscript)
        print("do\n", file=outscript)
        print(
            '     printf "',
            scriptshortname,
            ": Running test",
            ' (${testname})...\\n"',
            file=outscript,
        )
        print(
            '     printf "',
            scriptshortname,
            ": Command: ",
            " jsrun -p 1 python ",
            suitepath + "/${testname}.py ",
            resultsfilename,
            '\\n"\n',
            file=outscript,
        )
        print("     date\n", file=outscript)
        print(
            " jsrun -p 1 python ",
            suitepath + "/${testname}.py ",
            resultsfilename,
            "\n",
            file=outscript,
        )
        print("     date\n", file=outscript)
        print("done\n", file=outscript)
        outscript.close()
        os.chmod(spawnerpath, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        # Now the suite runner:
        outscript = open(scriptfilename, "w")
        numnodes = 1
        numprocjob = 1
#        numproctest = 1
        timeout = 10
        # print("#!/bin/bash\n\nset -x\ndate", file=outscript)
        print("#!/bin/bash\n\ndate", file=outscript)
        print(
            "lalloc "
            + str(numnodes)
#            + " -n "
#            + str(numprocjob)
            + " -W "
            + str(timeout)
            + " -q pdebug "
            + spawnerpath,
            file=outscript,
        )
        print("errorCode=$?", file=outscript)
        print("date", file=outscript)
        print("exit $errorCode", file=outscript)
        outscript.close()
        os.chmod(scriptfilename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

if __name__ == "__main__":

    suitepath = "./"
    outputpath = "./"
    suitename = "SerialTEESD"

    numargs = len(sys.argv)
    if numargs > 1:
        suitename = sys.argv[1]
    if numargs > 2:
        suitepath = sys.argv[2]
    if numargs > 3:
        outputpath = sys.argv[3]

    generate_suite_runner(suitename, suitepath, outputpath)