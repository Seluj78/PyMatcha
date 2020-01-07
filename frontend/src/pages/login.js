import React from 'react';
import { getToken } from "../utils"
import { useHistory } from "react-router-dom";

const logMe = (history, from) => () => {
	sessionStorage.setItem("token", "super token");
	history.push(from || "/")
}

const LoginCard = ({ history, from }) => (
	<article className="tile is-child notification is-info">
		<div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
			<div className="field">
				<p className="control has-icons-left">
					<input className="input is-info" type="text" placeholder="Email" style={{ backgroundColor: 'deepskyblue' }} />
					<span className="icon is-small is-left">
						<i className="fas fa-envelope" />
					</span>
				</p>
			</div>
			<div className="field">
				<p className="control has-icons-left">
					<input className="input is-info" type="password" placeholder="Password" style={{ backgroundColor: 'deepskyblue' }} />
					<span className="icon is-small is-left">
						<i className="fas fa-lock" />
					</span>
				</p>
			</div>
			<div className="field">
				<button className="button is-info is-light is-rounded" onClick={logMe(history, from)}> Log in </button>
			</div>
			<div className="field">
				<button className="button is-outlined is-warning is-rounded" > mot de passe oublier </button>
			</div>
		</div>
	</article>
)

// If oldPath is set, maybe a blur effect
const Login = ({ from }) => {
	const history = useHistory();
	if (!!getToken())
		history.push("/");
	return (
			<div className="container" style={{ textAlign: 'center', padding: '1.5em' }}>
				<p className="title is-1" style={{ margin: '1em' }} >Matcha</p>
				<div className="tile is-ancestor">
					<div className="tile is-vertical is-8">
						<div className="tile">
							<div className="tile is-parent is-vertical">
								<article className="tile is-child notification is-primary">
									<p className="subtitle">Guilhem 22 ans j'ai trouver l'ame soeur grace a ce site</p>
								</article>
								<article className="tile is-child notification is-warning">
									<p className="subtitle">Lea 34 ans, apres ma rupture avec mon copain matcha m'a redonne espoir</p>
								</article>
							</div>
							<div className="tile is-parent">
								<LoginCard history={history} from={from} />
							</div>
						</div>
						<div className="tile is-parent">
							<article className="tile is-child notification is-danger">
								<p className="subtitle">Matcha est plus qu'une page web c'est un lieu de magie, de rencontre, grace a nos algorythme pas du tout intrusif nous vous faisons rencontrer la personne dont vous revez la nuit</p>
								<div className="content">
								</div>
							</article>
						</div>
					</div>
					<div className="tile is-parent">
						<article className="tile is-child notification is-success">
							<div className="content">
								<p className="subtitle">formulaire d'inscription</p>
							</div>
						</article>
					</div>
				</div>
			</div>
	)
}

export default Login;