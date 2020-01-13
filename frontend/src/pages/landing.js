import React from 'react';
import { getToken } from '../utils';
import { useHistory } from 'react-router-dom';
import LoginCard from '../components/login_card';

// If oldPath is set, maybe a blur effect
const Landing = ({ from }) => {
	const history = useHistory();
	if (!!getToken())
		history.push('/');
	return (
			<div className='container' style={{ textAlign: 'center', padding: '1.5em' }}>
				<p className='title is-1' style={{ margin: '1em' }} >Matcha</p>
				<div className='tile is-ancestor'>
					<div className='tile is-vertical is-8'>
						<div className='tile'>
							<div className='tile is-parent is-vertical'>
								<article className='tile is-child notification is-primary'>
									<p className='subtitle'>Guilhem 22 ans j'ai trouver l'ame soeur grace a ce site</p>
								</article>
								<article className='tile is-child notification is-warning'>
									<p className='subtitle'>Lea 34 ans, apres ma rupture avec mon copain matcha m'a redonne espoir</p>
								</article>
							</div>
							<div className='tile is-parent' style={{overflow: 'hidden'}}>
								<article className='tile is-child notification is-info'>
									<LoginCard history={history} from={from} />
								</article>
							</div>
						</div>
						<div className='tile is-parent'>
							<article className='tile is-child notification is-danger'>
								<p className='subtitle'>Matcha est plus qu'une page web c'est un lieu de magie, de rencontre, grace a nos algorythme pas du tout intrusif nous vous faisons rencontrer la personne dont vous revez la nuit</p>
								<div className='content'>
								</div>
							</article>
						</div>
					</div>
					<div className='tile is-parent'>
						<article className='tile is-child notification is-success'>
							<div className='content'>
								<p className='subtitle'>formulaire d'inscription</p>
							</div>
						</article>
					</div>
				</div>
			</div>
	)
}

export default Landing;