import React, { useState } from 'react';
import { effectDuration } from '../utils';
import Loading from '../components/loadings';

const logMe = (history, setState, email, password, from) => async () => {
	setState('loading');
	// API call
	// sessionStorage.setItem('token', 'api call result');
}

const discard = side => {
	return ({
		overflow: 'hidden',
		...effectDuration(0.5),
		...(side === 'left' ? {marginLeft: '100%'} : {marginRight: '100%'})
	})
}

const LoginCard = ({ history, from }) => {
	const [state, setState] = useState('');

	return (
		<div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
			<div className='field' style={state === 'loading' ? discard('left') : {}}>
				<p className='control has-icons-left'>
					<input className='input is-info' type='text' placeholder='Email' style={{ backgroundColor: 'deepskyblue' }} />
					<span className='icon is-small is-left'>
						<i className='fas fa-envelope' />
					</span>
				</p>
			</div> 
			<Loading style={{position: 'absolute', left: '50%', top: '50%', opacity: state === 'loading' ? '1' : '0' , ...effectDuration(1) }} />
			<div className='field' style={state === 'loading' ? discard('rigth') : {}}>
				<p className='control has-icons-left'>
					<input className='input is-info' type='password' placeholder='Password' style={{ backgroundColor: 'deepskyblue' }} />
					<span className='icon is-small is-left'>
						<i className='fas fa-lock' />
					</span>
				</p>
			</div>
			<div className='field' style={state === 'loading' ? discard('left') : {}}>
				<button className='button is-info is-light is-rounded' onClick={logMe(history, setState, from)}> Log in </button>
			</div>
			<div className='field' style={state === 'loading' ? discard('rigth') : {}}>
				<button className='button is-outlined is-warning is-rounded' > mot de passe oublier </button>
			</div>
		</div>
	)
}

export default LoginCard;