import React from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import Home from "./pages/home";
import Landing from "./pages/landing";
import NotFound from "./pages/not_found"
import { getRefreshToken } from './utils'
import './App.css';

const App = () => (
	<BrowserRouter>
		<Switch>
			<PrivateRoute exact path="/" component={Home} />
			<Route exact path="/login" component={Landing} />
			<Route component={NotFound} />
		</Switch>
	</BrowserRouter>
);

const PrivateRoute = ({ component: Component, ...rest }) => (
	<Route {...rest}
		render={props =>
			(!!getRefreshToken() ? (
				<Component {...props} />
			) : (
					<Redirect to={{ pathname: `/login${window.location.search}`, state: { from: props.location } }} />
				))
		}
	/>
);

export default App;
