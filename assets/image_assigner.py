import os, random

IMAGES_PATH = "D:/Tesis/hospital-web/public/patient_images"
WEBSITE_PATH="patient_images"


OLD_IDS=['00171-1550762361.png', '00172-3535804389.png', '00173-3535804390.png', '00174-3535804391.png', '00175-3535804392.png', '00176-3535804393.png', '00177-3535804394.png', '00178-3535804395.png', '00179-3535804396.png', '00180-3535804397.png', '00181-3535804398.png', '00182-3535804399.png', '00183-3535804400.png', '00184-3535804401.png', '00185-3535804402.png', '00186-3535804403.png', '00187-3535804404.png', '00188-3535804405.png', '00189-3535804406.png', '00190-3535804407.png', '00191-3535804408.png', '00192-3535804409.png', '00193-3535804410.png', '00194-3535804411.png', '00195-3535804412.png', '00196-3535804413.png', '00197-3535804414.png', '00198-3535804415.png', '00199-3535804416.png', '00200-3535804417.png', '00201-3535804418.png', '00202-3535804419.png', '00203-3535804420.png', '00204-3535804421.png', '00205-3535804422.png', '00206-3535804423.png', '00207-3535804424.png', '00208-3535804425.png', '00209-3535804426.png', '00210-3535804427.png', '00211-3535804428.png']
YOUNG_ADULT_IDS=['00304-3825687799.png', '00305-3825687800.png', '00306-3825687801.png', '00307-3825687802.png', '00308-3825687803.png', '00309-3825687804.png', '00310-3825687805.png', '00311-3825687806.png', '00312-3825687807.png', '00313-3825687808.png', '00314-3825687809.png', '00315-3825687810.png', '00316-3825687811.png', '00317-3825687812.png', '00318-3825687813.png', '00319-3825687814.png', '00320-3825687815.png', '00321-3825687816.png', '00322-3825687817.png', '00323-3825687818.png', '00324-3825687819.png', '00325-3825687820.png', '00326-3825687821.png', '00327-3825687822.png', '00328-3825687823.png', '00329-3825687824.png', '00330-3825687825.png', '00331-3825687826.png', '00332-3825687827.png', '00333-3825687828.png', '00334-3825687829.png', '00335-3825687830.png', '00336-3825687831.png', '00337-3825687832.png', '00338-3825687833.png', '00339-3825687834.png', '00340-3825687835.png', '00341-3825687836.png', '00342-3825687837.png', '00343-3825687838.png', '00344-3825687839.png', '00345-3825687840.png', '00346-3825687841.png', '00347-3825687842.png', '00348-3825687843.png', '00349-3825687844.png', '00350-3825687845.png', '00351-3825687846.png']

FOLD_IDS=['00212-4119276769.png', '00213-4119276770.png', '00214-4119276771.png', '00215-4119276772.png', '00216-4119276773.png', '00217-4119276774.png', '00218-4119276775.png', '00219-4119276776.png', '00220-4119276777.png', '00221-4119276778.png', '00222-4119276779.png', '00223-4119276780.png', '00224-4119276781.png', '00225-4119276782.png', '00226-4119276783.png', '00227-4119276784.png', '00228-4119276785.png', '00229-4119276786.png', '00230-4119276787.png', '00231-4119276788.png', '00232-4119276789.png', '00233-4119276790.png', '00234-4119276791.png', '00235-4119276792.png', '00236-4119276793.png', '00237-4119276794.png', '00238-4119276795.png', '00239-4119276796.png', '00240-4119276797.png', '00241-4119276798.png', '00242-4119276799.png', '00243-4119276800.png', '00244-4119276801.png', '00245-4119276802.png', '00246-4119276803.png', '00247-4119276804.png', '00248-4119276805.png', '00249-4119276806.png', '00250-4119276807.png', '00251-4119276808.png']
FYOUNG_ADULT_IDS=['00252-3227040252.png', '00253-3862945.png', '00255-2205737851.png', '00256-2645178946.png', '00257-2645178947.png', '00258-2645178948.png', '00259-2645178949.png', '00260-2645178950.png', '00261-2645178951.png', '00262-2645178952.png', '00263-2645178953.png', '00264-2645178954.png', '00265-2645178955.png', '00266-2645178956.png', '00267-2645178957.png', '00268-2645178958.png', '00269-2645178959.png', '00270-2645178960.png', '00271-2645178961.png', '00272-2645178962.png', '00273-2645178963.png', '00274-2645178964.png', '00275-2645178965.png', '00276-2645178966.png', '00277-2645178967.png', '00278-2645178968.png', '00279-2645178969.png', '00280-2645178970.png', '00281-2645178971.png', '00282-2645178972.png', '00283-2645178973.png', '00284-2645178974.png', '00285-2645178975.png', '00286-2645178976.png', '00287-2645178977.png', '00288-2645178978.png', '00289-2645178979.png', '00290-2645178980.png', '00291-2645178981.png', '00292-2645178982.png', '00293-2645178983.png', '00294-2645178984.png', '00295-2645178985.png', '00296-2645178986.png', '00297-2645178987.png', '00298-2645178988.png', '00299-2645178989.png', '00300-2645178990.png', '00301-2645178991.png', '00302-2645178992.png', '00303-2645178993.png']

def assign_image(patient):
    if patient["sex"] == "M":
        if int(patient["age"]) > 50:
            patient["src"] = WEBSITE_PATH + "/male/old/"+random.choice(OLD_IDS)
        else:
            patient["src"] = WEBSITE_PATH + "/male/young_adult/"+random.choice(YOUNG_ADULT_IDS)
    else:
        if int(patient["age"]) > 50:
            patient["src"] = WEBSITE_PATH + "/female/old/"+random.choice(FOLD_IDS)
        else:
            patient["src"] = WEBSITE_PATH + "/female/young_adult/"+random.choice(FYOUNG_ADULT_IDS)
