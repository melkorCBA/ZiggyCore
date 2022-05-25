
param($mode, $modules)

#project paths
$condabase = 'C:\Users\melkorCba\anaconda3\Scripts\activate.bat C:\Users\melkorCba\anaconda3'
$main = 'C:\work\FYP\mainController\mainControl'
$tts = 'C:\work\FYP\TTS\tft'
$stt = 'C:\work\FYP\googleSpeechToText'
$faceRec = 'C:\work\FYP\FaceRocg\CLTFaceRecognitionBase'
$motor = 'C:\work\FYP\motorController'

# serve commands
$mainCmd = 'Scripts\activate && python src\main.py'
$ttsCmd =  'Scripts\activate && python src\main.py'
$sttCmd = 'Scripts\activate && python src\main.py'
$faceRecCmd = $condabase + ' && conda activate cltFaceRec1 && python src\main.py'
$motorCmd = 'Scripts\activate && python src\main.py'




function Activate-Module {
    param (
        $srcPath, $cm
    )

    powershell -Command "Start-Process 'cmd'  -ArgumentList '/k c: && cd $srcPath && $cm'"
}

if($modules -eq $null){
    
    switch($mode){
    

        start {
            Activate-Module -srcPath $tts -cm $ttsCmd;
            Start-Sleep -Seconds 5
            Activate-Module -srcPath $main -cm $mainCmd;
            Start-Sleep -Seconds 2
            Activate-Module -srcPath $stt -cm $sttCmd;
            Activate-Module -srcPath $faceRec -cm $faceRecCmd;
            Activate-Module -srcPath $motor -cm $motorCmd;
            Break
        }
   

    }
    return;
}

if($modules.Length -ge 1){
    Foreach($module in $modules){

        if($module -eq 'tts'){
            Activate-Module -srcPath $tts -cm $ttsCmd;
            Start-Sleep -Seconds 5
            continue;
        }


        if($module -eq 'main'){
            Activate-Module -srcPath $main -cm $mainCmd;
            continue;
        }

        

        if($module -eq 'stt'){
            Activate-Module -srcPath $stt -cm $sttCmd;
            continue;
        }

        if($module -eq 'faceRec'){
            Activate-Module -srcPath $faceRec -cm $faceRecCmd;
            continue;
        }

         if($module -eq 'motor'){
            Activate-Module -srcPath $motor -cm $motorCmd;
            continue;
        }
    }
    
    return
}





