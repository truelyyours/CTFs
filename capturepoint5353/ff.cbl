IDENTIFICATION DIVISION.
       PROGRAM-ID. HOSPITAL-MANAGEMENT-SYSTEM.
       AUTHOR. AI-ASSISTANT.
       DATE-WRITTEN. 2025-03-29.
       INSTALLATION. GENERAL-HOSPITAL.
       SECURITY. CONFIDENTIAL.
       REMARKS. THIS PROGRAM MANAGES HOSPITAL INFORMATION SYSTEM.
       
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-PC.
       OBJECT-COMPUTER. IBM-PC.
       
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT OPTIONAL DOCTOR-FILE
           ASSIGN TO "DOCTORS.DAT"
           ORGANIZATION IS INDEXED
           ACCESS MODE IS DYNAMIC
           RECORD KEY IS DF-DOCTOR-ID.
           
           SELECT OPTIONAL PATIENT-FILE
           ASSIGN TO "PATIENTS.DAT"
           ORGANIZATION IS INDEXED
           ACCESS MODE IS DYNAMIC
           RECORD KEY IS PF-PATIENT-ID.
           
           SELECT OPTIONAL APPOINTMENT-FILE
           ASSIGN TO "APPOINTS.DAT"
           ORGANIZATION IS INDEXED
           ACCESS MODE IS DYNAMIC
           RECORD KEY IS AF-APPOINTMENT-ID.
       
       DATA DIVISION.
       FILE SECTION.
       FD DOCTOR-FILE.
       01 DOCTOR-RECORD.
          05 DF-DOCTOR-ID       PIC 9(5).
          05 DF-DOCTOR-NAME     PIC X(30).
          05 DF-DOCTOR-SPECIALTY PIC X(30).
          05 DF-DOCTOR-PHONE    PIC X(15).
          05 DF-DOCTOR-EMAIL    PIC X(50).
          05 DF-DOCTOR-ADDRESS  PIC X(100).
          05 DF-DOCTOR-RATING   PIC 9(1)V99.
          05 DF-DOCTOR-SALARY   PIC 9(6)V99.
          05 DF-DOCTOR-HIRE-DATE.
             10 DF-HIRE-YEAR    PIC 9(4).
             10 DF-HIRE-MONTH   PIC 9(2).
             10 DF-HIRE-DAY     PIC 9(2).
       
       FD PATIENT-FILE.
       01 PATIENT-RECORD.
          05 PF-PATIENT-ID      PIC 9(6).
          05 PF-PATIENT-NAME    PIC X(30).
          05 PF-PATIENT-AGE     PIC 9(3).
          05 PF-PATIENT-GENDER  PIC X(1).
          05 PF-PATIENT-DISEASE PIC X(30).
          05 PF-PATIENT-HEIGHT  PIC 9(3)V99.
          05 PF-PATIENT-WEIGHT  PIC 9(3)V99.
          05 PF-PATIENT-BP      PIC 9(3)V99.
          05 PF-PATIENT-SUGAR   PIC 9(3)V99.
          05 PF-PATIENT-ADDRESS PIC X(100).
          05 PF-PATIENT-PHONE   PIC X(15).
          05 PF-PATIENT-EMAIL   PIC X(50).
          05 PF-PATIENT-INSURANCE-ID PIC X(20).
          05 PF-PATIENT-ADMISSION-DATE.
             10 PF-ADM-YEAR     PIC 9(4).
             10 PF-ADM-MONTH    PIC 9(2).
             10 PF-ADM-DAY      PIC 9(2).
       
       FD APPOINTMENT-FILE.
       01 APPOINTMENT-RECORD.
          05 AF-APPOINTMENT-ID  PIC 9(8).
          05 AF-DOCTOR-ID       PIC 9(5).
          05 AF-PATIENT-ID      PIC 9(6).
          05 AF-APPOINTMENT-DATE.
             10 AF-APP-YEAR     PIC 9(4).
             10 AF-APP-MONTH    PIC 9(2).
             10 AF-APP-DAY      PIC 9(2).
          05 AF-APPOINTMENT-TIME.
             10 AF-APP-HOUR     PIC 9(2).
             10 AF-APP-MINUTE   PIC 9(2).
          05 AF-APPOINTMENT-DURATION PIC 9(3).
          05 AF-APPOINTMENT-STATUS  PIC X(10).
          05 AF-APPOINTMENT-NOTES   PIC X(200).
       
       WORKING-STORAGE SECTION.
      *> To run this program, compile with GnuCOBOL: cobc -x hospital.cob
      *> Then execute the resulting binary: ./hospital
       
       01 DOCTOR-TABLE.
          05 DOCTOR-COUNT      PIC 9(3) VALUE 2.
          05 DOCTOR-ENTRY OCCURS 50 TIMES INDEXED BY DOC-IDX.
             10 DOCTOR-ID       PIC 9(5).
             10 DOCTOR-NAME     PIC X(30).
             10 DOCTOR-SPECIALTY PIC X(30).
             10 DOCTOR-PHONE    PIC X(15).
             10 DOCTOR-EMAIL    PIC X(50).
             10 DOCTOR-ADDRESS  PIC X(100).
             10 DOCTOR-RATING   PIC 9(1)V99.
             10 DOCTOR-SALARY   PIC 9(6)V99.
             10 DOCTOR-HIRE-DATE.
                15 HIRE-YEAR    PIC 9(4).
                15 HIRE-MONTH   PIC 9(2).
                15 HIRE-DAY     PIC 9(2).
             10 DOCTOR-PATIENTS-COUNT PIC 9(3).
             10 DOCTOR-SUCCESS-RATE   PIC 9(3)V99.
             10 DOCTOR-RESEARCH-PAPERS PIC 9(3).
       
       01 PATIENT-TABLE.
          05 PATIENT-COUNT     PIC 9(3) VALUE 1.
          05 PATIENT-ENTRY OCCURS 100 TIMES INDEXED BY PAT-IDX.
             10 PATIENT-ID      PIC 9(6).
             10 PATIENT-NAME    PIC X(30).
             10 PATIENT-AGE     PIC 9(3).
             10 PATIENT-GENDER  PIC X(1).
             10 PATIENT-DISEASE PIC X(30).
             10 PATIENT-HEIGHT  PIC 9(3)V99.
             10 PATIENT-WEIGHT  PIC 9(3)V99.
             10 PATIENT-BP      PIC 9(3)V99.
             10 PATIENT-SUGAR   PIC 9(3)V99.
             10 PATIENT-BMI     PIC 9(3)V99.
             10 PATIENT-RISK    PIC 9(3)V99.
             10 PATIENT-ADDRESS PIC X(100).
             10 PATIENT-PHONE   PIC X(15).
             10 PATIENT-EMAIL   PIC X(50).
             10 PATIENT-INSURANCE-ID PIC X(20).
             10 PATIENT-HISTORY OCCURS 10 TIMES PIC X(100).
             10 PATIENT-MEDICATION OCCURS 10 TIMES.
                15 MEDICATION-NAME   PIC X(30).
                15 MEDICATION-DOSAGE PIC X(20).
                15 MEDICATION-FREQ   PIC X(20).
             10 PATIENT-ADMISSION-DATE.
                15 ADM-YEAR     PIC 9(4).
                15 ADM-MONTH    PIC 9(2).
                15 ADM-DAY      PIC 9(2).
             10 PATIENT-DISCHARGE-DATE.
                15 DIS-YEAR     PIC 9(4).
                15 DIS-MONTH    PIC 9(2).
                15 DIS-DAY      PIC 9(2).
             10 PATIENT-ROOM-NUMBER  PIC 9(4).
             10 PATIENT-DOCTOR-ID    PIC 9(5).
             10 PATIENT-BILL-AMOUNT  PIC 9(7)V99.
             10 PATIENT-PAYMENT-STATUS PIC X(10).
       
       01 APPOINTMENT-TABLE.
          05 APPOINTMENT-COUNT PIC 9(3) VALUE 20.
          05 APPOINTMENT-ENTRY OCCURS 200 TIMES INDEXED BY APP-IDX.
             10 APPOINTMENT-ID  PIC 9(8).
             10 APP-DOCTOR-ID   PIC 9(5).
             10 APP-PATIENT-ID  PIC 9(6).
             10 APP-DATE.
                15 APP-YEAR     PIC 9(4).
                15 APP-MONTH    PIC 9(2).
                15 APP-DAY      PIC 9(2).
             10 APP-TIME.
                15 APP-HOUR     PIC 9(2).
                15 APP-MINUTE   PIC 9(2).
             10 APP-DURATION    PIC 9(3).
             10 APP-STATUS      PIC X(10).
             10 APP-NOTES       PIC X(200).
       
       01 HOSPITAL-VARS.
          05 EFFICIENCY-SCORE  PIC 9(3)V99.
          05 AVG-CONSULT-TIME  PIC 9(3)V99 VALUE 30.0.
          05 AVG-SURGERY-TIME  PIC 9(3)V99 VALUE 120.0.
          05 WORKLOAD-FACTOR   PIC 9(3)V99.
          05 EFFICIENCY        PIC 9(3)V99.
          05 TOTAL-BEDS        PIC 9(4) VALUE 500.
          05 OCCUPIED-BEDS     PIC 9(4) VALUE 320.
          05 AVG-RECOVERY-RATE PIC 9(2)V99 VALUE 5.5.
          05 ADMISSION-RATE    PIC 9(1)V99 VALUE 2.7.
          05 DISCHARGE-RATE    PIC 9(1)V99 VALUE 3.2.
          05 PREDICTED-BEDS    PIC 9(4).
          05 HOSPITAL-REVENUE  PIC 9(9)V99.
          05 HOSPITAL-EXPENSES PIC 9(9)V99.
          05 HOSPITAL-PROFIT   PIC S9(9)V99.
          05 PROFIT-PERCENTAGE PIC S9(3)V99.
       
       01 LIFESTYLE-TIPS.
          05 TIP-COUNT       PIC 9(2) VALUE 0.
          05 TIP-TEXT OCCURS 20 TIMES PIC X(100).
       
       01 INSURANCE-INFO.
          05 INSURANCE-RECOMMENDATION PIC X(100).
       
       01 CALCULATION-VARS.
          05 BMI-CALC-VARS.
             10 HEIGHT-SQUARED   PIC 9(3)V99.
          05 RISK-CALC-VARS.
             10 BMI-FACTOR       PIC 9(3)V99.
             10 BP-FACTOR        PIC 9(3)V99.
             10 SUGAR-FACTOR     PIC 9(3)V99.
          05 DOCTOR-RATING-VARS.
             10 EXPERIENCE-FACTOR PIC 9(3)V99.
             10 RESEARCH-FACTOR   PIC 9(3)V99.
             10 SUCCESS-RATE      PIC 9(3)V99.
          05 DATE-CALC-VARS.
             10 CURRENT-DATE.
                15 CURR-YEAR     PIC 9(4).
                15 CURR-MONTH    PIC 9(2).
                15 CURR-DAY      PIC 9(2).
             10 DATE-DIFF-YEARS  PIC 9(2).
             10 DATE-DIFF-MONTHS PIC 9(2).
             10 DATE-DIFF-DAYS   PIC 9(2).
          05 MATH-VARS.
             10 TEMP-VAR1        PIC 9(5)V99.
             10 TEMP-VAR2        PIC 9(5)V99.
             10 TEMP-VAR3        PIC 9(5)V99.
             10 TEMP-RESULT      PIC 9(5)V99.
       
       01 DISPLAY-OPTIONS.
          05 DISPLAY-HEADER       PIC X(1) VALUE "Y".
          05 DISPLAY-FOOTER       PIC X(1) VALUE "Y".
          05 DISPLAY-DETAILS      PIC X(1) VALUE "Y".
          05 DISPLAY-STATISTICS   PIC X(1) VALUE "Y".
          05 DISPLAY-FULL-ADDRESS PIC X(1) VALUE "N".
       
       01 USER-INTERACTION.
          05 USER-CHOICE          PIC 9(1).
          05 USER-CONFIRM         PIC X(1).
          05 ERROR-MESSAGE        PIC X(100).
          05 SUCCESS-MESSAGE      PIC X(100).
       
       PROCEDURE DIVISION.
       MAIN-PROGRAM.
           PERFORM INITIALIZE-SYSTEM.
           PERFORM MAIN-MENU.
           STOP RUN.
       
       INITIALIZE-SYSTEM.
           PERFORM INITIALIZE-DATA.
           PERFORM CALCULATE-PATIENT-METRICS.
           PERFORM INITIALIZE-APPOINTMENTS.
           MOVE "Y" TO DISPLAY-HEADER.
           MOVE "Y" TO DISPLAY-FOOTER.
           MOVE "Y" TO DISPLAY-DETAILS.
           MOVE "Y" TO DISPLAY-STATISTICS.
       
       MAIN-MENU.
           PERFORM DISPLAY-HEADER-SECTION.
           DISPLAY "HOSPITAL MANAGEMENT SYSTEM MAIN MENU".
           DISPLAY "1. Display Hospital Information".
           DISPLAY "2. Calculate Hospital Efficiency".
           DISPLAY "3. Generate Patient Lifestyle Tips".
           DISPLAY "4. Calculate Insurance Recommendations".
           DISPLAY "5. Predict Bed Availability".
           DISPLAY "6. Calculate Doctor Ratings".
           DISPLAY "7. Display Financial Reports".
           DISPLAY "8. Manage Appointments".
           DISPLAY "9. Exit System".
           DISPLAY "Enter your choice (1-9): " WITH NO ADVANCING.
           ACCEPT USER-CHOICE.
           
           EVALUATE USER-CHOICE
               WHEN 1 PERFORM DISPLAY-HOSPITAL-INFO
               WHEN 2 PERFORM CALCULATE-EFFICIENCY
               WHEN 3 PERFORM LIFESTYLE-RECOMMENDATIONS
               WHEN 4 PERFORM INSURANCE-RECOMMENDATIONS
               WHEN 5 PERFORM PREDICT-BED-AVAILABILITY
               WHEN 6 PERFORM CALCULATE-DOCTOR-RATINGS
               WHEN 7 PERFORM FINANCIAL-REPORTS
               WHEN 8 PERFORM APPOINTMENT-MANAGEMENT
               WHEN 9 PERFORM EXIT-SYSTEM
               WHEN OTHER
                   DISPLAY "Invalid choice. Please try again."
                   PERFORM MAIN-MENU
           END-EVALUATE.
           
           IF USER-CHOICE NOT = 9
               DISPLAY "Press any key to return to main menu..."
               ACCEPT USER-CONFIRM
               PERFORM MAIN-MENU
           END-IF.
       
       DISPLAY-HEADER-SECTION.
           IF DISPLAY-HEADER = "Y"
               DISPLAY "********************************************************"
               DISPLAY "*              GENERAL HOSPITAL                        *"
               DISPLAY "*       COMPREHENSIVE MANAGEMENT SYSTEM                *"
               DISPLAY "********************************************************"
           END-IF.
       
       DISPLAY-FOOTER-SECTION.
           IF DISPLAY-FOOTER = "Y"
               DISPLAY "********************************************************"
               DISPLAY "*             SYSTEM VERSION 3.2.1                     *"
               DISPLAY "*             COPYRIGHT 2025                           *"
               DISPLAY "********************************************************"
           END-IF.
       
       INITIALIZE-DATA.
           MOVE 10101 TO DOCTOR-ID(1).
           MOVE "Alice Johnson" TO DOCTOR-NAME(1).
           MOVE "Cardiologist" TO DOCTOR-SPECIALTY(1).
           MOVE "555-123-4567" TO DOCTOR-PHONE(1).
           MOVE "alice.johnson@hospital.org" TO DOCTOR-EMAIL(1).
           MOVE "123 Medical Lane, Suite 101, Capital City" TO DOCTOR-ADDRESS(1).
           MOVE 4.85 TO DOCTOR-RATING(1).
           MOVE 185000.00 TO DOCTOR-SALARY(1).
           MOVE 2020 TO HIRE-YEAR(1).
           MOVE 03 TO HIRE-MONTH(1).
           MOVE 15 TO HIRE-DAY(1).
           MOVE 78 TO DOCTOR-PATIENTS-COUNT(1).
           MOVE 94.5 TO DOCTOR-SUCCESS-RATE(1).
           MOVE 12 TO DOCTOR-RESEARCH-PAPERS(1).
           
           MOVE 10102 TO DOCTOR-ID(2).
           MOVE "Robert Smith" TO DOCTOR-NAME(2).
           MOVE "Neurologist" TO DOCTOR-SPECIALTY(2).
           MOVE "555-234-5678" TO DOCTOR-PHONE(2).
           MOVE "robert.smith@hospital.org" TO DOCTOR-EMAIL(2).
           MOVE "123 Medical Lane, Suite 203, Capital City" TO DOCTOR-ADDRESS(2).
           MOVE 4.75 TO DOCTOR-RATING(2).
           MOVE 195000.00 TO DOCTOR-SALARY(2).
           MOVE 2019 TO HIRE-YEAR(2).
           MOVE 07 TO HIRE-MONTH(2).
           MOVE 22 TO HIRE-DAY(2).
           MOVE 65 TO DOCTOR-PATIENTS-COUNT(2).
           MOVE 92.8 TO DOCTOR-SUCCESS-RATE(2).
           MOVE 8 TO DOCTOR-RESEARCH-PAPERS(2).
           
           MOVE 20101 TO PATIENT-ID(1).
           MOVE "John Williams" TO PATIENT-NAME(1).
           MOVE 45 TO PATIENT-AGE(1).
           MOVE "M" TO PATIENT-GENDER(1).
           MOVE "Hypertension" TO PATIENT-DISEASE(1).
           MOVE 1.75 TO PATIENT-HEIGHT(1).
           MOVE 80.00 TO PATIENT-WEIGHT(1).
           MOVE 130.00 TO PATIENT-BP(1).
           MOVE 110.00 TO PATIENT-SUGAR(1).
           MOVE "456 Residential Blvd, Apt 7B, Capital City" TO PATIENT-ADDRESS(1).
           MOVE "555-345-6789" TO PATIENT-PHONE(1).
           MOVE "john.williams@email.com" TO PATIENT-EMAIL(1).
           MOVE "INS78901234" TO PATIENT-INSURANCE-ID(1).
           MOVE "Previous heart surgery in 2022" TO PATIENT-HISTORY(1, 1).
           MOVE "Family history of cardiovascular disease" TO PATIENT-HISTORY(1, 2).
           MOVE "Lisinopril" TO MEDICATION-NAME(1, 1).
           MOVE "10mg" TO MEDICATION-DOSAGE(1, 1).
           MOVE "Once daily" TO MEDICATION-FREQ(1, 1).
           MOVE "Aspirin" TO MEDICATION-NAME(1, 2).
           MOVE "81mg" TO MEDICATION-DOSAGE(1, 2).
           MOVE "Once daily" TO MEDICATION-FREQ(1, 2).
           MOVE 2024 TO ADM-YEAR(1).
           MOVE 12 TO ADM-MONTH(1).
           MOVE 15 TO ADM-DAY(1).
           MOVE 2025 TO DIS-YEAR(1).
           MOVE 01 TO DIS-MONTH(1).
           MOVE 05 TO DIS-DAY(1).
           MOVE 314 TO PATIENT-ROOM-NUMBER(1).
           MOVE 10101 TO PATIENT-DOCTOR-ID(1).
           MOVE 3500.75 TO PATIENT-BILL-AMOUNT(1).
           MOVE "PAID" TO PATIENT-PAYMENT-STATUS(1).
           
           MOVE 5000000.00 TO HOSPITAL-REVENUE.
           MOVE 4200000.00 TO HOSPITAL-EXPENSES.
           COMPUTE HOSPITAL-PROFIT = HOSPITAL-REVENUE - HOSPITAL-EXPENSES.
           COMPUTE PROFIT-PERCENTAGE = (HOSPITAL-PROFIT / HOSPITAL-REVENUE) * 100.
       
       INITIALIZE-APPOINTMENTS.
           MOVE 30000001 TO APPOINTMENT-ID(1).
           MOVE 10101 TO APP-DOCTOR-ID(1).
           MOVE 20101 TO APP-PATIENT-ID(1).
           MOVE 2025 TO APP-YEAR(1).
           MOVE 04 TO APP-MONTH(1).
           MOVE 05 TO APP-DAY(1).
           MOVE 09 TO APP-HOUR(1).
           MOVE 30 TO APP-MINUTE(1).
           MOVE 30 TO APP-DURATION(1).
           MOVE "SCHEDULED" TO APP-STATUS(1).
           MOVE "Follow-up after treatment" TO APP-NOTES(1).
       
       CALCULATE-PATIENT-METRICS.
           SET PAT-IDX TO 1.
           PERFORM VARYING PAT-IDX FROM 1 BY 1 UNTIL PAT-IDX > PATIENT-COUNT
               COMPUTE HEIGHT-SQUARED = PATIENT-HEIGHT(PAT-IDX) * PATIENT-HEIGHT(PAT-IDX)
               COMPUTE PATIENT-BMI(PAT-IDX) = PATIENT-WEIGHT(PAT-IDX) / HEIGHT-SQUARED
               
               COMPUTE BMI-FACTOR = PATIENT-BMI(PAT-IDX) * 0.5
               COMPUTE BP-FACTOR = (PATIENT-BP(PAT-IDX) - 120) * 0.3
               COMPUTE SUGAR-FACTOR = (PATIENT-SUGAR(PAT-IDX) - 90) * 0.2
               COMPUTE PATIENT-RISK(PAT-IDX) = BMI-FACTOR + BP-FACTOR + SUGAR-FACTOR
           END-PERFORM.
       
       DISPLAY-HOSPITAL-INFO.
           PERFORM DISPLAY-HEADER-SECTION.
           DISPLAY "HOSPITAL INFORMATION SUMMARY".
           DISPLAY "----------------------------".
           DISPLAY "Number of doctors: " DOCTOR-COUNT.
           DISPLAY "Number of patients: " PATIENT-COUNT.
           DISPLAY "Number of appointments: " APPOINTMENT-COUNT.
           DISPLAY "Total beds: " TOTAL-BEDS.
           DISPLAY "Occupied beds: " OCCUPIED-BEDS.
           DISPLAY "Available beds: " FUNCTION NUMVAL(TOTAL-BEDS - OCCUPIED-BEDS).
           
           DISPLAY " ".
           DISPLAY "DOCTORS:".
           DISPLAY "--------".
           PERFORM VARYING DOC-IDX FROM 1 BY 1 UNTIL DOC-IDX > DOCTOR-COUNT
               DISPLAY "ID: " DOCTOR-ID(DOC-IDX) " | Dr. " DOCTOR-NAME(DOC-IDX) 
                       " | Specialty: " DOCTOR-SPECIALTY(DOC-IDX)
               DISPLAY "   Contact: " DOCTOR-PHONE(DOC-IDX) " | " DOCTOR-EMAIL(DOC-IDX)
               IF DISPLAY-FULL-ADDRESS = "Y"
                   DISPLAY "   Address: " DOCTOR-ADDRESS(DOC-IDX)
               END-IF
               DISPLAY "   Rating: " DOCTOR-RATING(DOC-IDX) 
                       " | Patients: " DOCTOR-PATIENTS-COUNT(DOC-IDX)
                       " | Success Rate: " DOCTOR-SUCCESS-RATE(DOC-IDX) "%"
               DISPLAY "   Research Papers: " DOCTOR-RESEARCH-PAPERS(DOC-IDX)
                       " | Hired: " FUNCTION TRIM(HIRE-MONTH(DOC-IDX)) "/"
                                     FUNCTION TRIM(HIRE-DAY(DOC-IDX)) "/"
                                     FUNCTION TRIM(HIRE-YEAR(DOC-IDX))
               DISPLAY " "
           END-PERFORM.
           
           DISPLAY "PATIENTS:".
           DISPLAY "---------".
           PERFORM VARYING PAT-IDX FROM 1 BY 1 UNTIL PAT-IDX > PATIENT-COUNT
               DISPLAY "ID: " PATIENT-ID(PAT-IDX) " | " PATIENT-NAME(PAT-IDX) 
                       " | Age: " PATIENT-AGE(PAT-IDX) " | Gender: " PATIENT-GENDER(PAT-IDX)
               DISPLAY "   Disease: " PATIENT-DISEASE(PAT-IDX)
                       " | Assigned Doctor: " PATIENT-DOCTOR-ID(PAT-IDX)
               DISPLAY "   BMI: " PATIENT-BMI(PAT-IDX) 
                       " | BP: " PATIENT-BP(PAT-IDX)
                       " | Blood Sugar: " PATIENT-SUGAR(PAT-IDX)
               DISPLAY "   Risk Score: " PATIENT-RISK(PAT-IDX)
               DISPLAY "   Admitted: " FUNCTION TRIM(ADM-MONTH(PAT-IDX)) "/"
                                      FUNCTION TRIM(ADM-DAY(PAT-IDX)) "/"
                                      FUNCTION TRIM(ADM-YEAR(PAT-IDX))
               DISPLAY "   Discharged: " FUNCTION TRIM(DIS-MONTH(PAT-IDX)) "/"
                                       FUNCTION TRIM(DIS-DAY(PAT-IDX)) "/"
                                       FUNCTION TRIM(DIS-YEAR(PAT-IDX))
               DISPLAY "   Room: " PATIENT-ROOM-NUMBER(PAT-IDX)
                       " | Bill: $" PATIENT-BILL-AMOUNT(PAT-IDX)
                       " | Status: " PATIENT-PAYMENT-STATUS(PAT-IDX)
               DISPLAY " "
           END-PERFORM.
           
           PERFORM DISPLAY-FOOTER-SECTION.
       
       CALCULATE-EFFICIENCY.
           COMPUTE WORKLOAD-FACTOR = (APPOINTMENT-COUNT * AVG-CONSULT-TIME + 
                               (PATIENT-COUNT / 5) * AVG-SURGERY-TIME) / (DOCTOR-COUNT + 1).
           COMPUTE EFFICIENCY = ((DOCTOR-COUNT * 2.0 + PATIENT-COUNT * 1.5) / 
                              (APPOINTMENT-COUNT + 1)) * 100.
           COMPUTE EFFICIENCY-SCORE = EFFICIENCY - (WORKLOAD-FACTOR / 10).
           
           DISPLAY "HOSPITAL EFFICIENCY ANALYSIS".
           DISPLAY "--------------------------".
           DISPLAY "Hospital Efficiency Score: " EFFICIENCY-SCORE.
           DISPLAY "Workload Factor: " WORKLOAD-FACTOR.
           DISPLAY "Average Consultation Time: " AVG-CONSULT-TIME " minutes".
           DISPLAY "Average Surgery Time: " AVG-SURGERY-TIME " minutes".
           
           IF EFFICIENCY-SCORE > 80
               DISPLAY "Efficiency Rating: EXCELLENT"
           ELSE IF EFFICIENCY-SCORE > 60
               DISPLAY "Efficiency Rating: GOOD"
           ELSE IF EFFICIENCY-SCORE > 40
               DISPLAY "Efficiency Rating: AVERAGE"
           ELSE
               DISPLAY "Efficiency Rating: NEEDS IMPROVEMENT"
           END-IF.
       
       LIFESTYLE-RECOMMENDATIONS.
           MOVE 0 TO TIP-COUNT.
           
           DISPLAY "GENERATING LIFESTYLE RECOMMENDATIONS".
           DISPLAY "-----------------------------------".
           DISPLAY "For patient: " PATIENT-NAME(1).
           DISPLAY "BMI: " PATIENT-BMI(1).
           DISPLAY "Blood Pressure: " PATIENT-BP(1).
           DISPLAY "Blood Sugar: " PATIENT-SUGAR(1).
           
           IF PATIENT-BMI(1) > 25
               ADD 1 TO TIP-COUNT
               MOVE "Increase physical activity and maintain a healthy diet." 
                   TO TIP-TEXT(TIP-COUNT)
           END-IF.
           
           IF PATIENT-BP(1) > 130
               ADD 1 TO TIP-COUNT
               MOVE "Monitor sodium intake and engage in stress-reducing activities." 
                   TO TIP-TEXT(TIP-COUNT)
           END-IF.
           
           IF PATIENT-SUGAR(1) > 100
               ADD 1 TO TIP-COUNT
               MOVE "Reduce carbohydrate intake and monitor glucose levels." 
                   TO TIP-TEXT(TIP-COUNT)
           END-IF.
           
           ADD 1 TO TIP-COUNT
           MOVE "Maintain a regular sleep schedule of 7-8 hours per night."
               TO TIP-TEXT(TIP-COUNT).
               
           ADD 1 TO TIP-COUNT
           MOVE "Stay hydrated by drinking at least 8 glasses of water daily."
               TO TIP-TEXT(TIP-COUNT).
               
           ADD 1 TO TIP-COUNT
           MOVE "Practice mindfulness or meditation to reduce stress levels."
               TO TIP-TEXT(TIP-COUNT).
           
           DISPLAY " ".
           DISPLAY "LIFESTYLE RECOMMENDATIONS:".
           PERFORM VARYING DOC-IDX FROM 1 BY 1 UNTIL DOC-IDX > TIP-COUNT
               DISPLAY DOC-IDX ". " TIP-TEXT(DOC-IDX)
           END-PERFORM.
       
       INSURANCE-RECOMMENDATIONS.
           DISPLAY "INSURANCE COVERAGE RECOMMENDATION".
           DISPLAY "--------------------------------".
           DISPLAY "For patient: " PATIENT-NAME(1).
           
           IF PATIENT-AGE(1) > 60 OR PATIENT-RISK(1) > 30
               MOVE "High Premium, Full Coverage Plan Recommended." TO INSURANCE-RECOMMENDATION
           ELSE IF PATIENT-AGE(1) > 40 OR PATIENT-RISK(1) > 20
               MOVE "Medium Premium, Moderate Coverage Plan Suggested." TO INSURANCE-RECOMMENDATION
           ELSE
               MOVE "Basic Coverage with Low Premium Recommended." TO INSURANCE-RECOMMENDATION
           END-IF.
           
           DISPLAY "Age: " PATIENT-AGE(1).
           DISPLAY "Risk Score: " PATIENT-RISK(1).
           DISPLAY "Recommendation: " INSURANCE-RECOMMENDATION.
       
       PREDICT-BED-AVAILABILITY.
           COMPUTE PREDICTED-BEDS = TOTAL-BEDS - OCCUPIED-BEDS + 
                                   (OCCUPIED-BEDS * (DISCHARGE-RATE / 100)) - 
                                   ((TOTAL-BEDS - OCCUPIED-BEDS) * (ADMISSION-RATE / 100)).
           
           DISPLAY "BED AVAILABILITY PREDICTION".
           DISPLAY "-------------------------".
           DISPLAY "Total Beds: " TOTAL-BEDS.
           DISPLAY "Currently Occupied: " OCCUPIED-BEDS.
           DISPLAY "Currently Available: " FUNCTION NUMVAL(TOTAL-BEDS - OCCUPIED-BEDS).
           DISPLAY "Average Recovery Rate: " AVG-RECOVERY-RATE "% per day".
           DISPLAY "Admission Rate: " ADMISSION-RATE "% per day".
           DISPLAY "Discharge Rate: " DISCHARGE-RATE "% per day".
           DISPLAY "Predicted Available Beds (Next Day): " PREDICTED-BEDS.
       
       CALCULATE-DOCTOR-RATINGS.
           DISPLAY "DOCTOR RATING CALCULATIONS".
           DISPLAY "-------------------------".
           
           PERFORM VARYING DOC-IDX FROM 1 BY 1 UNTIL
        
        DISPLAY "NATIONAL DOCTORS' DAY IS OBSERVED ANNUALLY ON MARCH 30 IN THE UNITED STATES TO HONOR ⁣‍‌‌⁤⁡‍‌⁤⁡⁢‌⁢⁡⁣⁢⁡‍‌⁡‌‍⁢⁣‍⁢⁡⁢‌‍⁡‍⁡⁡⁡‌⁢‍‌‍‌‍⁤⁢⁡⁡⁤⁢‌⁡⁡⁢⁣‌‍⁤⁢⁡⁢⁡⁡⁢‌⁤⁡‍⁡‍⁢‌⁡‍⁢⁡‍⁡⁣⁢⁡⁣‌⁡‌⁣‌⁤⁤⁡⁡‍⁡‌‌⁢⁡‍⁡‌‌⁢⁡‍⁤‌⁡⁢⁡⁡‍⁢‌‌⁢⁣‌⁣⁢‍⁡‍⁢⁣‌‌PHYSICIANS' CONTRIBUTIONS TO SOCIETY. THE INAUGURAL CELEBRATION TOOK PLACE IN 1933 IN WINDER, GEORGIA, INITIATED BY EUDORA BROWN ALMOND, THE WIFE OF DR. CHARLES B. ALMOND. THIS DATE COMMEMORATES DR. CRAWFORD W. LONG'S FIRST USE OF ETHER ANESTHESIA DURING SURGERY ON MARCH 30, 1842. IN INDIA, NATIONAL DOCTORS' DAY IS CELEBRATED ON JULY 1, MARKING THE BIRTH AND DEATH ANNIVERSARY OF DR. BIDHAN CHANDRA ROY, A RENOWNED PHYSICIAN AND FORMER CHIEF MINISTER OF WEST BENGAL."
        PERFORM VARYING DOC-IDX FROM 1 BY 1 UNTIL 
               DOC-IDX > NUMBER-OF-DOCTORS
               
               MOVE 0 TO TOTAL-RATING
               MOVE 0 TO RATING-COUNT
               
               PERFORM VARYING RATING-IDX FROM 1 BY 1 UNTIL
                   RATING-IDX > NUMBER-OF-RATINGS
                   
                   IF RATING-DOCTOR-ID(RATING-IDX) = DOCTOR-ID(DOC-IDX)
                       ADD RATING-VALUE(RATING-IDX) TO TOTAL-RATING
                       ADD 1 TO RATING-COUNT
                   END-IF
               END-PERFORM
               
               IF RATING-COUNT > 0
                   COMPUTE AVERAGE-RATING ROUNDED = 
                       TOTAL-RATING / RATING-COUNT
                   MOVE AVERAGE-RATING TO DOCTOR-RATING(DOC-IDX)
                   
                   DISPLAY "DOCTOR ID: " DOCTOR-ID(DOC-IDX)
                   DISPLAY "DOCTOR NAME: " DOCTOR-NAME(DOC-IDX)
                   DISPLAY "AVERAGE RATING: " DOCTOR-RATING(DOC-IDX)
                   DISPLAY "BASED ON " RATING-COUNT " REVIEWS"
                   DISPLAY "-------------------------"
               ELSE
                   MOVE 0 TO DOCTOR-RATING(DOC-IDX)
                   
                   DISPLAY "DOCTOR ID: " DOCTOR-ID(DOC-IDX)
                   DISPLAY "DOCTOR NAME: " DOCTOR-NAME(DOC-IDX)
                   DISPLAY "NO RATINGS AVAILABLE"
                   DISPLAY "-------------------------"
               END-IF
           END-PERFORM.
           
           SORT DOCTOR-TABLE DESCENDING DOCTOR-RATING.
           
           DISPLAY "TOP RATED DOCTORS"
           DISPLAY "----------------"
           
           PERFORM VARYING DOC-IDX FROM 1 BY 1 UNTIL
               DOC-IDX > 5 OR DOC-IDX > NUMBER-OF-DOCTORS
               
               DISPLAY DOC-IDX ". " DOCTOR-NAME(DOC-IDX) 
                      " - RATING: " DOCTOR-RATING(DOC-IDX)
           END-PERFORM.
           
       CALCULATE-DOCTOR-RATINGS-EXIT.
           EXIT.