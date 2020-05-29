import React from "react";
import { useHistory } from "react-router-dom";
import { getRefreshToken, getAccessToken } from "../utils"

const OnboardingPage = () => {
	const history = useHistory();

	if (!getRefreshToken())
		history.push('/login');
	if (localStorage.getItem("onboarding") !== "true")
		history.push('/');

	return <p>Onboarding</p>
}

export default OnboardingPage;