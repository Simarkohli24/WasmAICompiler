import difflib
from hashlib import new
from imp import reload
import os 
import random 
import numpy as np
from IPython.display import clear_output
import pickle
from random import random
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import pandas as pd 
import time
import random
import subprocess

#### success criterion = line difference of 14
def compareFiles(File1,File2):
    d=set(File1.readlines())
    e=set(File2.readlines())
 #Create the file
    x = []
    for line in list(d-e):
        x.append(line)
    return x

def _make_gen(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024*1024)

def rawpycount(filename):
    f = open(filename, 'rb')
    f_gen = _make_gen(f.raw.read)
    return sum( buf.count(b'\n') for buf in f_gen )
  
def checkLogFiles(txtfile, first): 
  
  os.chdir('..')
  os.chdir('..')

  output = None
  c = None
  while(output is None): 
    c= open(txtfile, 'rb')
    output = len(c.readlines())
  os.chdir('crate/pkg')
  return c, output

def getAvgSpeed(numTrials, lclNum): 
  total = 0
  min = 100
  max = 0
  cur = 0
  failedInstances = 0
  successYet = False
  while (cur < numTrials):
    driver = Chrome(executable_path= '/Users/simar/Desktop/GIthub-Issue-Bot/chromedriver')
    driver.get('http://localhost:' + str(lclNum))
    u = random.randint(1,10)
    v = random.randint(1,10)
    try: 
      a = driver.find_element(By.XPATH, '/html/body/div/div/div[' + str(u) + ']/div[' + str(v) + ']')
      w = time.perf_counter()
      a.click()
      x = time.perf_counter()
      y = x-w
      total = total + y
      if (y < min): 
        min = y
      if (y > max): 
        max = y 
      cur = cur + 1
      successYet = True
    except: 
      if (failedInstances > 10 and successYet == False):
        return -11; 
      failedInstances = failedInstances + 1
      pass
  return (total/numTrials) 

def stepAction(state, speedNum, filename, optimization, currentEpisodeStep, maxEpisodeSteps, lclNum, verbose=False):

  prevTime = getAvgSpeed(speedNum, lclNum)
  fileFirst, lenFirst = checkLogFiles('stuff.txt', True)
  if (state != 0): 
    subprocess.call(["/Users/simar/Downloads/binaryen-version_110/bin/wasm-opt", "-O", "--" + optimization, "-o", filename, filename ])
  else:
    subprocess.call(["/Users/simar/Downloads/binaryen-version_110/bin/wasm-opt", "-O", "--" + optimization, "-o", filename, "OG_index_bg.wasm" ])
  fileSecond, lenSecond = checkLogFiles('stuff.txt', False)
  fileSizeDifference = lenSecond - lenFirst
  newTime = getAvgSpeed(speedNum, lclNum)
  reward = prevTime-newTime
  if (fileSizeDifference >= 21): 
    print("Attempted " + optimization + "." + " ERROR occured.")
    return -11, -11, True
  if verbose:
    print("Applied " + optimization)
    print(prevTime)
    print(newTime)
    print("Reward: " + str(reward))
    print("----------------------")
  done = False;
  if (currentEpisodeStep == maxEpisodeSteps):
    done = True;
  return reward, newTime, done 

def training(filename, alpha, gamma, epsil, maxEpisodeSteps, lclNum, speedNum, verbose): 
  alpha = alpha
  gamma = gamma 
  epsil = epsil 
  og_epsil = epsil
  maxEpisodeSteps = maxEpisodeSteps
  filename = filename 
  stateActionSpace = {}
  stateActionSpace[0] = np.zeros(len(optimization_space))

  min_state_space = {}
  min_speed = 1000
  temp_speed = 1000

  for i in range(1, 50001): 
    state = 0;
    epochs, penalties, reward = 0,0,0
    currentEpisodeStep = 0;
    done = False
    print(i)
    if (i % 10 == 0):
      epsil = 0.9
    else:
      epsil = og_epsil
    while not done: 
      if (random.uniform(0,1) < epsil):
        action_num = random.randint(0, len(optimization_space)-1)
        action = optimization_space[action_num]; 
      else: 
        action_num = np.argmax(stateActionSpace[state])
        action = optimization_space[action_num]
      currentEpisodeStep = currentEpisodeStep + 1
      reward, cur_speed, done = stepAction(state, speedNum, filename, action, currentEpisodeStep, maxEpisodeSteps, lclNum, verbose)
      if (cur_speed < 0.3): 
          print("this is fucked, we need to fix this")
          print(action)
          done = True
      if (not done):
        next_state = state + 1; 
        old_value = stateActionSpace[state][action_num]
        if (next_state not in stateActionSpace):
          stateActionSpace[next_state] = np.zeros(len(optimization_space))
        next_max = np.max(stateActionSpace[next_state])
        if (reward < 0 and reward > -0.03): 
          reward = 0
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        stateActionSpace[state][action_num] = new_value
        if reward < 0: 
          penalties+=1
        state = next_state
        epochs+=1
        if (cur_speed < min_speed and cur_speed > 0.3): 
          print("minimum speed has been detected: " + str(cur_speed))
          temp_speed = cur_speed
        if (cur_speed < min_speed and cur_speed > 0.3 and (abs(temp_speed - cur_speed) < 0.1)): 
          min_speed = cur_speed
          print("minimum speed has been detected and verified: " + str(cur_speed))
          min_state_space = stateActionSpace
          f = open("stateSpace.pkl","wb")
          pickle.dump(min_state_space,f)
          f.close(); 
          temp_speed=1000

    if i % 100 == 0:
        clear_output(wait=True)
        print(f"Episode: {i}")

train = True
test = True
metrics = not True
manualRun = not True

if (train):
  # ==================== OS adjustments ==================== #
  subprocess.run(['ls'])
  os.chdir('tic-tac-toe-wasm-master/crate/pkg')
  print("here")
  # subprocess.run(["cd", "tic-tac-toe-wasm-master/crate/pkg"])
  # ======================================================== #

  # ==================== GlobalVariables =================== #
  optimization_space = ["alignment-lowering","asyncify","avoid-reinterprets","cfp","coalesce-locals","coalesce-locals-learning","code-folding","code-pushing","const-hoisting","dae","dae-optimizing","dce","dealign","denan","dfo","directize","duplicate-function-elimination","duplicate-import-elimination","dwarfdump","emit-target-features","flatten","generate-dyncalls","generate-i64-dyncalls","generate-stack-ir","global-refining","gsi","gto","gufa","gufa-optimizing","heap2local","i64-to-i32-lowering","inline-main","inlining","inlining-optimizing","instrument-locals","instrument-memory","intrinsic-lowering","legalize-js-interface","legalize-js-interface-minimally","licm","limit-segments","local-cse","local-subtyping","log-execution","memory-packing","memory64-lowering","merge-blocks","merge-locals","merge-similar-functions","mod-asyncify-always-and-only-unwind","mod-asyncify-never-unwind","name-types","once-reduction","optimize-added-constants","optimize-added-constants-propagate","optimize-for-js","optimize-instructions","optimize-stack-ir","pick-load-signs","poppify","post-emscripten","precompute","precompute-propagate","remove-memory","remove-non-js-ops","remove-unused-brs","remove-unused-module-elements","remove-unused-names","remove-unused-nonfunction-module-elements","reorder-functions","reorder-locals","rereloop","roundtrip","rse","safe-heap","set-globals","signature-pruning","signature-refining","simplify-globals","simplify-globals-optimizing","simplify-locals","simplify-locals-nonesting","simplify-locals-nostructure","simplify-locals-notee","simplify-locals-notee-nostructure","ssa","ssa-nomerge","stack-check","strip","strip-debug","strip-dwarf","strip-producers","strip-target-features","stub-unsupported-js","trap-mode-clamp","trap-mode-js","type-refining","untee","vacuum"]

  filename = "index_bg.wasm"
  alpha = 0.1
  gamma = 0.6
  epsil = 0.3
  maxEpisodeSteps = 50
  localHostNumber = 8080
  speedTrials = 3 
  # ======================================================== #
  # subprocess.run(['ls'])
  # subprocess.run(['rm', 'index_bg.wasm'])
  # subprocess.run(["cp", "OG_" + filename, filename])
  # ==================== BeginTraining ===================== #
  training(filename, alpha, gamma, epsil, maxEpisodeSteps, localHostNumber, speedTrials, True)
  # ======================================================== #
else:
  optimization_space = ["alignment-lowering","asyncify","avoid-reinterprets","cfp","coalesce-locals","coalesce-locals-learning","code-folding","code-pushing","const-hoisting","dae","dae-optimizing","dce","dealign","denan","dfo","directize","duplicate-function-elimination","duplicate-import-elimination","dwarfdump","emit-target-features","flatten","generate-dyncalls","generate-i64-dyncalls","generate-stack-ir","global-refining","gsi","gto","gufa","gufa-optimizing","heap2local","i64-to-i32-lowering","inline-main","inlining","inlining-optimizing","instrument-locals","instrument-memory","intrinsic-lowering","legalize-js-interface","legalize-js-interface-minimally","licm","limit-segments","local-cse","local-subtyping","log-execution","memory-packing","memory64-lowering","merge-blocks","merge-locals","merge-similar-functions","mod-asyncify-always-and-only-unwind","mod-asyncify-never-unwind","name-types","once-reduction","optimize-added-constants","optimize-added-constants-propagate","optimize-for-js","optimize-instructions","optimize-stack-ir","pick-load-signs","poppify","post-emscripten","precompute","precompute-propagate","remove-memory","remove-non-js-ops","remove-unused-brs","remove-unused-module-elements","remove-unused-names","remove-unused-nonfunction-module-elements","reorder-functions","reorder-locals","rereloop","roundtrip","rse","safe-heap","set-globals","signature-pruning","signature-refining","simplify-globals","simplify-globals-optimizing","simplify-locals","simplify-locals-nonesting","simplify-locals-nostructure","simplify-locals-notee","simplify-locals-notee-nostructure","ssa","ssa-nomerge","stack-check","strip","strip-debug","strip-dwarf","strip-producers","strip-target-features","stub-unsupported-js","trap-mode-clamp","trap-mode-js","type-refining","untee","vacuum"]
  setter = set()
  outputAssociations = {}
  for i in range(0,len(optimization_space)):
    a = False
    os.chdir('tic-tac-toe-wasm-master/crate/pkg')
    os.chdir('..')
    os.chdir('..')
    output = None
    b = None

    while(output is None): 
      b = open('stuff.txt', 'rb')
      output = len(b.readlines())
    
    os.chdir('crate/pkg')
    step = ["code-folding", "const-hoisting", "intrinsic-lowering", "gufa", "simplify-locals-notee"]
    filename = "index_bg.wasm"
    x = subprocess.call(["/Users/simar/Downloads/binaryen-version_110/bin/wasm-opt", "-O", "--" + optimization_space[i], "-o", filename, "OG_index_bg.wasm" ])
    os.chdir('..')
    os.chdir('..')
    output2 = None
    c = None
    while(output2 is None): 
      c = open('stuff.txt', 'rb')
      output2 = len(c.readlines())
    setter.add(output2-output)
    d = difflib.Differ()
    diff = d.compare(b.readlines(), c.readlines())
    minioutput = "\n".join(diff)
    os.chdir('..')
    if (output2-output) in outputAssociations: 
      outputAssociations[output2 - output].append(minioutput)
    else:
      outputAssociations[output2 - output] = [minioutput] 
    
    # f = open("stateSpace.pkl", 'rb')
    # reloadSpace = pickle.load(f)
  # print(reloadSpace)
  for element in setter:
    i = 0
    for e in outputAssociations[element]: 
      if (i < 4): 
        print("=======")
        print("Difference number: " + str(element))
        print(e)
        print("=======")
        i = i + 1 
    
  # print(outputAssociations)
if test: 
  filename = "IR_index_bg.wasm"
  f = open("stateSpace.pkl", 'rb')
  reloadSpace = pickle.load(f)
  optimization_space = ["alignment-lowering","asyncify","avoid-reinterprets","cfp","coalesce-locals","coalesce-locals-learning","code-folding","code-pushing","const-hoisting","dae","dae-optimizing","dce","dealign","denan","dfo","directize","duplicate-function-elimination","duplicate-import-elimination","dwarfdump","emit-target-features","flatten","generate-dyncalls","generate-i64-dyncalls","generate-stack-ir","global-refining","gsi","gto","gufa","gufa-optimizing","heap2local","i64-to-i32-lowering","inline-main","inlining","inlining-optimizing","instrument-locals","instrument-memory","intrinsic-lowering","legalize-js-interface","legalize-js-interface-minimally","licm","limit-segments","local-cse","local-subtyping","log-execution","memory-packing","memory64-lowering","merge-blocks","merge-locals","merge-similar-functions","mod-asyncify-always-and-only-unwind","mod-asyncify-never-unwind","name-types","once-reduction","optimize-added-constants","optimize-added-constants-propagate","optimize-for-js","optimize-instructions","optimize-stack-ir","pick-load-signs","poppify","post-emscripten","precompute","precompute-propagate","remove-memory","remove-non-js-ops","remove-unused-brs","remove-unused-module-elements","remove-unused-names","remove-unused-nonfunction-module-elements","reorder-functions","reorder-locals","rereloop","roundtrip","rse","safe-heap","set-globals","signature-pruning","signature-refining","simplify-globals","simplify-globals-optimizing","simplify-locals","simplify-locals-nonesting","simplify-locals-nostructure","simplify-locals-notee","simplify-locals-notee-nostructure","ssa","ssa-nomerge","stack-check","strip","strip-debug","strip-dwarf","strip-producers","strip-target-features","stub-unsupported-js","trap-mode-clamp","trap-mode-js","type-refining","untee","vacuum"]

  for i in range(0,len(reloadSpace)):
    print(i)
    optimization_num = np.argmax(reloadSpace[i])
    optimization = optimization_space[optimization_num]
    if (i != 0): 
      subprocess.call(["/Users/simar/Downloads/binaryen-version_110/bin/wasm-opt", "-O", "--" + optimization, "-o", filename, filename ])
    else:
      subprocess.call(["/Users/simar/Downloads/binaryen-version_110/bin/wasm-opt", "-O", "--" + optimization, "-o", filename, "OG_index_bg.wasm" ])
if metrics:
  filename = "index_bg.wasm"
  print(getAvgSpeed(10, localHostNumber))
  subprocess.run(['rm', 'index_bg.wasm'])
  subprocess.run(["cp", "OG_" + filename, filename])
  print(getAvgSpeed(10, localHostNumber))

if manualRun: 
  # os.chdir('tic-tac-toe-wasm-master/crate/pkg')
  filename = "index_bg.wasm"
  i = 0
  optimizationSteps = ["code-folding", "const-hoisting", "intrinsic-lowering", "gufa", "simplify-locals-notee", "generate-stack-ir", "heap2local", "optimize-for-js"]
  for step in optimizationSteps: 
    print(i)
    if (i != 0): 
      subprocess.call(["/Users/simar/Downloads/binaryen-version_110/bin/wasm-opt", "-O", "--" + step, "-o", filename, filename ])
    else:
      i = 1
      subprocess.call(["/Users/simar/Downloads/binaryen-version_110/bin/wasm-opt", "-O", "--" + step, "-o", filename, "OG_index_bg.wasm"])
  print(getAvgSpeed(10, localHostNumber))
  