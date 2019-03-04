Sub Multi_Year_Breakdown()

    Dim ws As Worksheet
    
    For Each ws In ThisWorkbook.Sheets
    
        ws.Activate
    
            Dim Ticker As String
            Dim TickCol As Long
            Dim TotalVolume As Double
            Dim VolCol As Long
            Dim LastRow As Long
            Dim LastCol As Long
            Dim i As Long
            Dim SummaryRow As Long
            Dim OpenPrice As Double
            Dim OpenCol As Long
            Dim ClosePrice As Double
            Dim CloseCol As Long
            Dim YearChange As Double
            Dim PercChange As Double
            
            
            TickCol = 1
            VolCol = 7
            OpenCol = 3
            CloseCol = 6
            SummaryRow = 2
            TotalVolume = 0
            OpenPrice = Range("C2").Value
        
            LastRow = Cells(Rows.Count, 1).End(xlUp).Row
            LastCol = Cells(1, Columns.Count).End(xlToLeft).Column
            
            Cells(1, LastCol + 2).Value = "Ticker"
            Cells(1, LastCol + 3).Value = "Yearly Change"
            Cells(1, LastCol + 4).Value = "Percent Change"
            Cells(1, LastCol + 5).Value = "Total Stock Volume"
            
            Cells(2, LastCol + 3) = OpenPrice
            
            For i = 2 To LastRow
             
                If Cells(i + 1, TickCol).Value <> Cells(i, TickCol).Value Then
                
                    Ticker = Cells(i, TickCol).Value
                    
                    TotalVolume = TotalVolume + Cells(i, VolCol).Value
                    
                    ClosePrice = Cells(i, CloseCol).Value
                    
                        If OpenPrice = ClosePrice Then
                        
                            YearChange = 0
                        
                            PercChange = 0
                            
                        ElseIf OpenPrice = 0 Then
                        
                            YearChange = ClosePrice
                            
                            PercChange = 0
                            
                        Else
                        
                            YearChange = ClosePrice - OpenPrice
                    
                            PercChange = (YearChange / OpenPrice)
                    
                        End If
                    
                    
                    Cells(SummaryRow, LastCol + 2) = Ticker
                    
                    Cells(SummaryRow, LastCol + 3) = YearChange
                    
                        Cells(SummaryRow, LastCol + 3).NumberFormat = "0.000000000"
                    
                    Cells(SummaryRow, LastCol + 4).Value = PercChange
                    
                        Cells(SummaryRow, LastCol + 4).NumberFormat = "0.00%"
                    
                    Cells(SummaryRow, LastCol + 5) = TotalVolume
                    
                    
                    If YearChange > 0 Then
                        
                        Cells(SummaryRow, LastCol + 3).Interior.ColorIndex = 4
                
                    ElseIf YearChange < 0 Then
                    
                        Cells(SummaryRow, LastCol + 3).Interior.ColorIndex = 3
                        
                    End If
                    
                    
                    SummaryRow = SummaryRow + 1
                    
                    OpenPrice = Cells(i + 1, OpenCol)
                    
                    TotalVolume = 0
                    
                    
                Else
                
                    TotalVolume = TotalVolume + Cells(i, VolCol).Value
                    
                
                End If
                   
             Next i
             
             
             Dim GreatPercInc As Double
             Dim GreatPercDec As Double
             Dim GreatVolume As Double
             Dim Count As Integer
             Dim MinTick As String
             Dim MaxTick As String
             Dim MaxVolTick As String
    
             Min = 1000
             Max = -1000
             MaxVol = -1000
             SummaryRow = 2
    
             LastCol = Cells(1, Columns.Count).End(xlToLeft).Column
    
             Cells(1, LastCol + 3).Value = "Ticker"
             Cells(1, LastCol + 4).Value = "Value"
    
             Cells(SummaryRow, LastCol + 2).Value = "Greatest % Increase"
             Cells(SummaryRow + 1, LastCol + 2).Value = "Greatest % Decrease"
             Cells(SummaryRow + 2, LastCol + 2).Value = "Greatest Volume"
    
             For i = SummaryRow To LastRow
    
                If Min > Cells(SummaryRow, 11) Then
                    Min = Cells(SummaryRow, 11)
                    MinTick = Cells(SummaryRow, 9)
    
                End If
    
                If Max < Cells(SummaryRow, 11) Then
                    Max = Cells(SummaryRow, 11)
                    MaxTick = Cells(SummaryRow, 9)
    
                End If
                
                If MaxVol < Cells(SummaryRow, 12) Then
                    MaxVol = Cells(SummaryRow, 12)
                    MaxVolTick = Cells(SummaryRow, 9)
    
                End If
    
                SummaryRow = SummaryRow + 1
    
             Next i
    
            Range("P2").Value = Max
            Range("P3").Value = Min
                Range("P2:P3").NumberFormat = "0.00%"
            Range("P4").Value = MaxVol
            
            Range("O2").Value = MaxTick
            Range("O3").Value = MinTick
            Range("O4").Value = MaxVolTick
            
        ActiveSheet.UsedRange.Columns.AutoFit
    
    Next ws
        
End Sub
