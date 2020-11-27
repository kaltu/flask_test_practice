*** Settings ***
Library  Selenium2Library

*** Variables ***
${HOMEPAGE}  http://127.0.0.1
${BROWSER}  chrome
${USERNAME}  admin
${PASSWORD}  admin

*** Keywords ***
open the browser
  Open Browser  ${HOMEPAGE}  ${BROWSER}

wait and input
  [Arguments]  ${locator}  ${text}
  Wait Until Element Is Visible  ${locator}
  Input Text  ${locator}  ${text}

wait and click
  [Arguments]  ${locator}
  Wait Until Element Is Visible   ${locator}
  Click Element  ${locator}

wait and check
  [Arguments]  ${locator}  ${text}
  Wait Until Element Is Visible  ${locator}
  Element Text Should Be  ${locator}  ${text}

check login
  wait and input  id=username  ${USERNAME}
  wait and input  id=password  ${PASSWORD}
  wait and click  id=submit
  wait and check  id=msg  login success

check wrong credential
  wait and input  id=username  ${USERNAME}
  wait and input  id=password  123
  wait and click  id=submit
  wait and check  id=msg  login failed

check blank fields
  wait and click  id=submit
  wait and check  id=msg  login failed

*** Test Cases ***
Open browser and run
  open the browser

Check blank
  check blank fields

Check login
  check login

Check wrong
  check wrong credential
