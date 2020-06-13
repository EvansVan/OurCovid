def estimator(data):
  current = data["reportedCases"]
  timeElapsed = data["timeToElapse"]
  period = data["periodType"]
  beds = data["totalHospitalBeds"]
  income = data['region']['avgDailyIncomeInUSD']
  incomePopulation = data['region']['avgDailyIncomePopulation']

  impact_currentlyInfected = 10 * current
  severeImpact_currentlyInfected = 50 * current

  #calculate infections by required time
  def task1(stuff):
      if period == 'days':
          days = timeElapsed
      elif period == 'weeks':
          days = timeElapsed * 7
      elif period == 'months':
          days = timeElapsed * 30
      days = days // 3
      return stuff * (2 ** days)

  #calculate severe cases by required time
  def task2(stuff):
    return 0.15 * task1(stuff)

  #calculate beds required by time
  def task3(stuff):
    availableBeds = 0.35 * beds
    return int(availableBeds - task2(stuff))

  #calculate money lost to economy
  def task4(stuff):
    if period == 'days':
        days = timeElapsed
    elif period == 'weeks':
        days = timeElapsed * 7
    elif period == 'months':
        days = timeElapsed * 30
    mult = task1(stuff)
    return int((mult * income * incomePopulation) / days)

  results = {
      "data": data,
      "impact": {
          "currentlyInfected": impact_currentlyInfected,
          "infectionsByRequestedTime": task1(impact_currentlyInfected),
          "severeCasesByRequestedTime": int(task2(impact_currentlyInfected)),
          "hospitalBedsByRequestedTime": task3(impact_currentlyInfected),
          "casesForICUByRequestedTime": int(0.05 * task1(impact_currentlyInfected)),
          "casesForVentilatorsByRequestedTime": int(0.02 * task1(impact_currentlyInfected)),
          "dollarsInFlight": task4(impact_currentlyInfected)
      },
      "severeImpact": {
          "currentlyInfected": severeImpact_currentlyInfected,
          "infectionsByRequestedTime": task1(severeImpact_currentlyInfected),
          "severeCasesByRequestedTime": int(task2(severeImpact_currentlyInfected)),
          "hospitalBedsByRequestedTime": task3(severeImpact_currentlyInfected),
          "casesForICUByRequestedTime": int(0.05 * task1(severeImpact_currentlyInfected)),
          "casesForVentilatorsByRequestedTime": int(0.02 * task1(severeImpact_currentlyInfected)),
          "dollarsInFlight": task4(severeImpact_currentlyInfected)
      }
  }
  return results
