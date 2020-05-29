import React from 'react';
import { BrowserRouter, Switch, Route, Redirect, useHistory } from 'react-router-dom';
import Home from "./pages/home";
import Landing from "./pages/landing";
import Onboarding from "./pages/onboarding";
import NotFound from "./pages/not_found";
import { getRefreshToken } from './utils';
import './App.css';

const App = () => (
	<BrowserRouter>
		<Switch>
			<PrivateRoute exact path="/" component={Home} />
			<Route exact path="/onboarding" component={Onboarding} />
			<Route exact path="/login" component={Landing} />
			<Route component={NotFound} />
		</Switch>
	</BrowserRouter>
);

const PrivateRoute = ({ component: Component, ...rest }) => {
	const history = useHistory();

	return (
		<Route {...rest}
			render={props => {
				if (!getRefreshToken()) return <Redirect to={{ pathname: `/login${window.location.search}`, state: { from: props.location } }} />
				else if (localStorage.getItem("onboarding") === "true") return <Redirect to={{ pathname: `/onboarding`, state: { from: props.location } }} />
				return <Component {...props} />
			}} />
	)
}

export default App;
