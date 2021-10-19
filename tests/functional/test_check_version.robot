# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

*** Settings ***
Documentation			Tests for the semantic version check.
Library					Collections
Library					Process
Suite Teardown			Terminate All Processes	kill=True

*** Keywords ***
Run Mantic
	[Arguments]			@{args}
	${result} =			Run Process
	...					poetry		run		mantic
	... 				@{args}
	...					alias=mantic
	...					env:COLUMNS=200
	...					stdout=.robot/stdout.txt
	[Return]			${result}

Exit OK
	@{exit_codes}					Create List			${0}	${1}	${2}	${3}
	[Arguments]						${exit_code}
	List Should Contain Value		${exit_codes}		${exit_code}

*** Test Cases ***
Prints the help screen to the user.
	${result} =			Run Mantic		--help  check-version
	Wait For Process	mantic
	Should Contain		${result.stdout}	Usage: mantic check-version [--options] …
	Should Contain		${result.stdout}	Check if the actual version is valid.
	Should Contain		${result.stdout}	-i, --ignore
	Should Contain		${result.stdout}	Paths to ignore
	Should Contain		${result.stdout}	.editorconfig, .github
	Exit OK				${result.rc}

Checks for required version bump.
	${result} =			Run Mantic		check-version
	Wait For Process	mantic
	Exit OK				${result.rc}
