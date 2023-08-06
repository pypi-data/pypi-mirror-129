Function OnCalculation()
         Dim ppm_ee ' DBO5, DCO, MES, COT, MG
         ppm_sortie  = Array(2.4,55,8.3,40.5,9) ' ppm eau de sortie
        Module.OutputStream(1).MolarFlowrate =  Module.InputStream(1).MolarFlowrate
        ' calcul de l'eau de sortie
        with Module.OutputStream(1)
        xw = 1 ' fraction eau
        For i=1 to 5
                xw = xw -   ppm_sortie(i-1) /1e6
               .PartialMolarFlowrate(i+1) =  .MolarFlowrate*ppm_sortie(i-1) /1e6
        Next
        .PartialMolarFlowrate(1) =  .MolarFlowrate*xw 'water
       end with
       OnCalculation = true
End Function