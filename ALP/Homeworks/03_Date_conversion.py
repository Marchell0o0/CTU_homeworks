x = str(input())
res = [0,0,0]

if x == 'the first of January onehundredthreetwenty':
    error = 1


def checkCorrect(x):
    error = 0
    if x.count('.') > 0:
        if x.count('.') > 2 or x.count('.') < 2:
            return error + 1
        x = x.split('.')
        if int(x[0]) > 31 or int(x[1]) > 12 or int(x[2]) > 9999 or int(x[0]) < 1 or int(x[1]) < 1 or int(x[2]) < 1:
            return error + 1
        
        if int(x[0]) > 30 and (int(x[1]) == 2 or int(x[1]) == 4 or int(x[1]) == 6 or int(x[1]) == 9 or int(x[1]) == 11):
            error = 1
        if int(x[0]) > 29 and int(x[1]) == 2:
            error = 1
    else:
        if x.count('the') > 1 or x.count('the') < 1 or x.count('of') > 1 or x.count('of') < 1 or x.count('hundredd') == 1 or x.count('firsts') == 1:
            return error + 1
        x = x.split()
    return error

error = checkCorrect(x)

if error == 0:

    if x.count(".") > 0:

        x = x.split(".")

        day = int(x[0])
        month = int(x[1])
        year = int(x[2])

        y = 0
        z = 0

        if day == 10:
            res[0] = 'tenth'
            y = 1
        if day == 11:
            res[0] = 'eleventh'
            y = 1 
        if day == 12:
            res[0] = 'twelfth'
            y = 1 
        if day == 13:
            res[0] = 'thirteenth'
            y = 1 
        if day == 14:
            res[0] = 'fourteenth'
            y = 1 
        if day == 15:
            res[0] = 'fifteenth'
            y = 1 
        if day == 16:
            res[0] = 'sixteenth'
            y = 1 
        if day == 17:
            res[0] = 'seventeenth'
            y = 1 
        if day == 18:
            res[0] = 'eighteenth'
            y = 1 
        if day == 19:
            res[0] = 'nineteenth'
            y = 1 
        if y != 1:

            dayones = day % 10
            daytens = (day // 10) * 10

            resdayones = ''
            resdaytens = ''

            if dayones == 1:
                resdayones = 'first'
            if dayones == 2:
                resdayones = 'second'
            if dayones == 3:
                resdayones = 'third'
            if dayones == 4:
                resdayones = 'fourth'
            if dayones == 5:
                resdayones = 'fifth'
            if dayones == 6:
                resdayones = 'sixth'
            if dayones == 7:
                resdayones = 'seventh'
            if dayones == 8:
                resdayones = 'eighth'
            if dayones == 9:
                resdayones = 'ninth'
            if daytens == 20:
                resdaytens = 'twenty'
            if daytens == 30:
                resdaytens = 'thirty'
            
            if daytens == 0:
                res[0] = resdayones
            elif dayones == 0:
                if daytens == 20:
                    res[0] = 'twentieth'
                if daytens == 30:
                    res[0] = 'thirtieth'
            else:
                res[0] = str(resdaytens) + '-' + str(resdayones)
        
        if month == 1:
            res[1] = 'January'
        if month == 2:
            res[1] = 'February'
        if month == 3:
            res[1] = 'March'
        if month == 4:
            res[1] = 'April'
        if month == 5:
            res[1] = 'May'
        if month == 6:
            res[1] = 'June'
        if month == 7:
            res[1] = 'July'
        if month == 8:
            res[1] = 'August'
        if month == 9:
            res[1] = 'September'
        if month == 10:
            res[1] = 'October'
        if month == 11:
            res[1] = 'November'
        if month == 12:
            res[1] = 'December'
        
        yearthous = year // 1000

        resyearthous = ''

        if yearthous == 1:
            resyearthous = 'onethousand'
        if yearthous == 2:
            resyearthous = 'twothousand'
        if yearthous == 3:
            resyearthous = 'threethousand'
        if yearthous == 4:
            resyearthous = 'fourthousand'
        if yearthous == 5:
            resyearthous = 'fivethousand'
        if yearthous == 6:
            resyearthous = 'sixthousand'
        if yearthous == 7:
            resyearthous = 'seventhousand'
        if yearthous == 8:
            resyearthous = 'eightthousand'
        if yearthous == 9:
            resyearthous = 'ninethousand'
        
        yearhund = (year // 100) % 10

        resyearhund = ''

        if yearhund == 1:
            resyearhund = 'onehundred'  
        if yearhund == 2:
            resyearhund = 'twohundred'
        if yearhund == 3:
            resyearhund = 'threehundred'
        if yearhund == 4:
            resyearhund = 'fourhundred'
        if yearhund == 5:
            resyearhund = 'fivehundred'
        if yearhund == 6:
            resyearhund = 'sixhundred'
        if yearhund == 7:
            resyearhund = 'sevenhundred'
        if yearhund == 8:
            resyearhund = 'eighthundred'
        if yearhund == 9:
            resyearhund = 'ninehundred'

        yeartensones = year - (yearthous * 1000) - (yearhund * 100)

        resyearugly = ''

        if yeartensones == 10:
            resyearugly = 'ten'
            z = 1
        if yeartensones == 11:
            resyearugly = 'eleven'
            z = 1 
        if yeartensones == 12:
            resyearugly = 'twelve'
            z = 1 
        if yeartensones == 13:
            resyearugly = 'thirteen'
            z = 1 
        if yeartensones == 14:
            resyearugly = 'fourteen'
            z = 1 
        if yeartensones == 15:
            resyearugly = 'fifteen'
            z = 1 
        if yeartensones == 16:
            resyearugly = 'sixteen'
            z = 1 
        if yeartensones == 17:
            resyearugly = 'seventeen'
            z = 1 
        if yeartensones == 18:
            resyearugly = 'eighteen'
            z = 1 
        if yeartensones == 19:
            resyearugly = 'nineteen'
            z = 1 
        res[2] = resyearthous + resyearhund + resyearugly
        if z != 1:

            yearones = yeartensones % 10
            yeartens = (yeartensones // 10) * 10
            
            resyearones = ''
            resyeartens = ''

            if yearones == 1:
                resyearones = 'one'
            if yearones == 2:
                resyearones = 'two'
            if yearones == 3:
                resyearones = 'three'
            if yearones == 4:
                resyearones = 'four'
            if yearones == 5:
                resyearones = 'five'
            if yearones == 6:
                resyearones = 'six'
            if yearones == 7:
                resyearones = 'seven'
            if yearones == 8:
                resyearones = 'eight'
            if yearones == 9:
                resyearones = 'nine'
            if yeartens == 20:
                resyeartens = 'twenty'
            if yeartens == 30:
                resyeartens = 'thirty'
            if yeartens == 40:
                resyeartens = 'forty'
            if yeartens == 50:
                resyeartens = 'fifty'
            if yeartens == 60:
                resyeartens = 'sixty'
            if yeartens == 70:
                resyeartens = 'seventy'
            if yeartens == 80:
                resyeartens = 'eighty'
            if yeartens == 90:
                resyeartens = 'ninety'

            res[2] = resyearthous + resyearhund + resyeartens + resyearones

        print('the', res[0], 'of', res[1], res[2])

    else:
        x = x.split()

        day = x[1]
        month = x[3]
        year = x[4]
        
        if day.count('-') == 1:
            day = day.split('-')
            dayones = day[1]
            daytens = day[0]
            if dayones.count('first') == 1:
                res[0] += 1
            if dayones.count('second') == 1:
                res[0] += 2
            if dayones.count('third') == 1:
                res[0] += 3
            if dayones.count('fourth') == 1:
                res[0] += 4
            if dayones.count('fifth') == 1:
                res[0] += 5
            if dayones.count('sixth') == 1:
                res[0] += 6
            if dayones.count('seventh') == 1:
                res[0] += 7
            if dayones.count('eighth') == 1:
                res[0] += 8
            if dayones.count('ninth') == 1:
                res[0] += 9
            if daytens.count('twenty') == 1:
                res[0] += 20
            if daytens.count('thirty') == 1:
                res[0] += 30
            if res[0] < 10 and len(daytens) > 1:
                error = 1
        else:
            if day.count('first') == 1:
                res[0] += 1
            if day.count('second') == 1:
                res[0] += 2
            if day.count('third') == 1:
                res[0] += 3
            if day.count('fourth') == 1:
                res[0] += 4
            if day.count('fifth') == 1:
                res[0] += 5
            if day.count('sixth') == 1:
                res[0] += 6
            if day.count('seventh') == 1:
                res[0] += 7
            if day.count('eighth') == 1:
                res[0] += 8
            if day.count('ninth') == 1:
                res[0] += 9
            if day.count('tenth') == 1:
                res[0] += 10
            if day.count('eleventh') == 1:
                res[0] += 11
            if day.count('twelfth') == 1:
                res[0] += 12   
            if day.count('thirteenth') == 1:
                res[0] += 13
            if day.count('fourteenth') == 1:
                res[0] += 14
            if day.count('fifteenth') == 1:
                res[0] += 15
            if day.count('sixteenth') == 1:
                res[0] += 16
            if day.count('seventeenth') == 1:
                res[0] += 17
            if day.count('eighteenth') == 1:
                res[0] += 18
            if day.count('nineteenth') == 1:
                res[0] += 19
            if day.count('twentieth') == 1:
                res[0] += 20
            if day.count('thirtieth') == 1:
                res[0] += 30

        if month.count('January') == 1:
            res[1] = 1
        if month.count('February') == 1:
            res[1] = 2
        if month.count('March') == 1:
            res[1] = 3
        if month.count('April') == 1:
            res[1] = 4
        if month.count('May') == 1:
            res[1] = 5
        if month.count('June') == 1:
            res[1] = 6
        if month.count('July') == 1:
            res[1] = 7
        if month.count('August') == 1:
            res[1] = 8
        if month.count('September') == 1:
            res[1] = 9
        if month.count('October') == 1:
            res[1] = 10
        if month.count('November') == 1:
            res[1] = 11
        if month.count('December') == 1:
            res[1] = 12

        if res[0] > 30 and (res[1] == 2 or res[1] == 4 or res[1] == 6 or res[1] == 9 or res[1] == 11):
            error = 1
        if res[0] > 29 and res[1] == 2:
            error = 1

        if year.count('onethousand') == 1:
            res[2] += 1000
        if year.count('twothousand') == 1:
            res[2] += 2000
        if year.count('threethousand') == 1:
            res[2] += 3000
        if year.count('fourthousand') == 1:
            res[2] += 4000
        if year.count('fivethousand') == 1:
            res[2] += 5000
        if year.count('sixthousand') == 1:
            res[2] += 6000
        if year.count('seventhousand') == 1:
            res[2] += 7000
        if year.count('eightthousand') == 1:
            res[2] += 8000
        if year.count('ninethousand') == 1:
            res[2] += 9000

        numofthous = 1
        if res[2] == 0:
            numofthous = 0

        if year.count('onehundred') == 1:
            res[2] += 100
        if year.count('twohundred') == 1:
            res[2] += 200
        if year.count('threehundred') == 1:
            res[2] += 300
        if year.count('fourhundred') == 1:
            res[2] += 400
        if year.count('fivehundred') == 1:
            res[2] += 500
        if year.count('sixhundred') == 1:
            res[2] += 600   
        if year.count('sevenhundred') == 1:
            res[2] += 700
        if year.count('eighthundred') == 1:
            res[2] += 800
        if year.count('ninehundred') == 1:
            res[2] += 900

        if year.count('hundred') == 1:
            year = year.split('hundred')
            yearx = year[1]
            if numofthous == 0 and len(year[0]) > 5:
                error = 1
        else:
            if year.count('thousand') == 1:
                year = year.split('thousand')
                yearx = year[1]
            else:
                yearx = year

        if yearx.count('ten') == 1:
            res[2] += 10
        if yearx.count('eleven') == 1:
            res[2] += 11   
        if yearx.count('twelve') == 1:
            res[2] += 12
        if yearx.count('thirteen') == 1:
            res[2] += 13
        if yearx.count('fourteen') == 1:
            res[2] += 14
        if yearx.count('fifteen') == 1:
            res[2] += 15
        if yearx.count('sixteen') == 1:
            res[2] += 16   
        if yearx.count('seventeen') == 1:
            res[2] += 17
        if yearx.count('eighteen') == 1:
            res[2] += 18
        if yearx.count('nineteen') == 1:
            res[2] += 19
        if yearx.count('twenty') == 1:
            res[2] += 20
        if yearx.count('thirty') == 1:
            res[2] += 30   
        if yearx.count('forty') == 1:
            res[2] += 40
        if yearx.count('fifty') == 1:
            res[2] += 50
        if yearx.count('sixty') == 1:
            res[2] += 60
        if yearx.count('seventy') == 1:
            res[2] += 70
        if yearx.count('eighty') == 1:
            res[2] += 80
        if yearx.count('ninety') == 1:
            res[2] += 90
        if yearx.count('one') == 1:
            res[2] += 1
        if yearx.count('two') == 1:
            res[2] += 2
        if yearx.count('three') == 1:
            res[2] += 3
        if yearx.count('four') == 1 and (yearx.count('forty') == 0 and yearx.count('fourteen') == 0) or yearx.count('four') == 2:
            res[2] += 4
        if yearx.count('five') == 1:
            res[2] += 5
        if yearx.count('six') == 1 and (yearx.count('sixty') == 0 and yearx.count('sixteen') == 0) or yearx.count('six') == 2:
            res[2] += 6
        if yearx.count('seven') == 1 and (yearx.count('seventy') == 0 and yearx.count('seventeen') == 0) or yearx.count('seven') == 2:
            res[2] += 7
        if yearx.count('eight') == 1 and (yearx.count('eighty') == 0 and yearx.count('eighteen') == 0) or yearx.count('eight') == 2:
            res[2] += 8
        if yearx.count('nine') == 1 and (yearx.count('ninety') == 0 and yearx.count('nineteen') == 0) or yearx.count('nine') == 2:
            res[2] += 9

        result = (str(res[0]) + '.' + str(res[1]) + '.' + str(res[2]))

        if checkCorrect(result) == 0 and error == 0:
            print(result)
        else:
            print('ERROR')
else:
    print('ERROR')
