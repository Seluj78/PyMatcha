import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { getRefreshToken, getAccessToken } from "../utils"

/*
	step:
	 - Orientation - age - description
	 - tags
	 - photos
*/

const orientations = ['heterosexual', 'homosexual', 'bisexual', 'other'];
const gender = ['male', 'female', 'other'];

const Meta = (form, setForm) => (
	<div>
		<hr class="hr" />
		<div className="field is-horizontal">
			<div className="field-label is-normal">
				<label className="label">Gender:</label>
			</div>
			<div className="field-body">
				<div className="field is-grouped-centered ">
					<p className="control">
						<span className="select" style={{ width: "100%" }}>
							<select style={{ width: "100%" }}>
								{gender.map((x, key) => <option key={key}>{x}</option>)}
							</select>
						</span>
					</p>
				</div>
				<div className="field-label is-normal">
					<label className="label">Orientation:</label>
				</div>
				<div className="field">
					<p className="control">
						<span className="select" style={{ width: "100%" }}>
							<select style={{ width: "100%" }}>
								{orientations.map((x, key) => <option key={key}>{x}</option>)}
							</select>
						</span>
					</p>
				</div>
				<div className="field-label is-normal">
					<label className="label">Age:</label>
				</div>
				<div className="field">
					<div className="control">
						<input className="input" type="number" />
					</div>
				</div>
			</div>
		</div>
		<div className="field is-horizontal">
			<div className="field-label is-normal">
				<label className="label">Description:</label>
			</div>
			<div className="field-body">
				<div className="field">
					<div className="control">
						<textarea className="textarea" placeholder="Explain how we can help you"></textarea>
					</div>
				</div>
			</div>
		</div>
	</div>
)
const Tags = () => (
	<div>
		<hr class="hr" />

		<div className="field is-horizontal is-grouped-centered">
			<div className="field-label is-normal">
				<label className="label">Description:</label>
			</div>
			<div className="field-body">
				<div class="field has-addons" style={{ flexGrow: "0" }}>
					<div class="control">
						<input class="input" type="text" placeholder="Enter a tag" />
					</div>
					<div class="control">
						<a class="button is-info">
							OK
					</a>
					</div>
				</div>
				<div class="tags">
					<span class="tag">
						Bar
				<button class="delete is-small"></button>
					</span>
					<span class="tag">
						Two
				<button class="delete is-small"></button>
					</span>
					<span class="tag">
						Three
				<button class="delete is-small"></button>
					</span>
				</div>
			</div>
		</div>
	</div>
)
const Photos = () => (
	<div>
		<hr class="hr" />
		<div class="card">
			<div class="card-image">
				<figure class="image">
					<img src="https://bulma.io/images/placeholders/1280x960.png" />
				</figure>
			</div>
		</div>
		<div class="field">
			<div class="file is-boxed" style={{ justifyContent: "center" }}>
				<label class="file-label">
					<input class="file-input" type="file" name="resume" />
					<span class="file-cta">
						<span class="file-icon">
							<i class="fas fa-cloud-upload-alt"></i>
						</span>
						<span class="file-label">
							Ajouter une image
						</span>
					</span>
				</label>
			</div>
		</div>
	</div>
)

const pages = [
	Meta,
	Tags,
	Photos
]

const inputState = setState => (name, value) => setState(state => { state[name] = value; return { ...state }; })

const OnboardingPage = () => {
	const history = useHistory();
	const [page, setPage] = useState(0);
	const [form, setForm] = useState({});

	if (!getRefreshToken())
		history.push('/login');
	if (localStorage.getItem("onboarding") !== "true")
		history.push('/');

	return (
		<div>
			<h1 className="title">On Baording</h1>
			<div className="content">
				<div className="mobile">
					{pages[page](form, inputState(setForm))}
				</div>
				<div className="desktop">
					{pages.map(page => page(form, inputState))}
				</div>
			</div>
			<hr class="hr" />
			<div className="mobile">
				<div style={{ display: "flex", justifyContent: "space-around" }}>
					<p class="control" onClick={() => setPage(state => state - (state < 1 ? 0 : 1))}>
						<a class="button is-light">
							Precedent
					</a>
					</p>
					<p class="control" onClick={() => setPage(state => state + (state + 1 > pages.length ? 0 : 1))}>
						<a class="button is-primary">
							Suivant
					</a>
					</p>
				</div>
			</div>
			<div className="desktop">
				<p class="control" style={{ textAlign: "center" }}>
					<a class="button is-primary">
						Suivant
					</a>
				</p>
			</div>
		</div>
	)
}

export default OnboardingPage;