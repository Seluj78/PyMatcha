import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { getRefreshToken, date2Html, apiCall } from "../utils";
import Loading from "./../components/loading"

/*
	step:
	 - Orientation - age - description
	 - tags
	 - photos
*/

const minimum_age = 364.25 * 24 * 60 * 60 * 18;
const orientations = ['heterosexual', 'homosexual', 'bisexual', 'other'];
const genders = ['male', 'female', 'other'];

const verify_entry = (form, setError) => {
	let errors = [];
	if (!form.gender)
		form.gender = genders[0]
	if (!form.orientation)
		form.orientation = orientations[0]
	if (!genders.includes(form.gender))
		errors.push("Invalid gender")
	if (!orientations.includes(form.orientation))
		errors.push("Invalid orientation")
	if (!form.birthdate)
		errors.push("Please enter you birthdate")
	if (Date.now() - form.birthdate < minimum_age)
		errors.push("You are too young you naughty boy")
	if ((form.tags || []).length < 3)
		errors.push("Please specify more tags (3 minimum)")
	if (!!errors.length) {
		setError(errors)
		window.scrollTo({ top: 0, behavior: 'smooth' });
		return false;
	}
	return form;
}

const Errors = ({ errors }) => {
	if (!errors || !errors.length) return ''
	return (
		<div style={{ marginBottom: "2em" }}>
			{errors.map((error, key) => (
				<div key={key} className="notification is-danger is-light" style={{ paddingTop: "0.5em", paddingBottom: "0.5em", marginBottom: "0.75em" }}>
					{error}
				</div>
			))
			}
		</div >
	)
}

const Meta = (form, setForm, key) => (
	<div key={key}>
		<hr className="hr" />
		<div className="field is-horizontal">
			<div className="field-label is-normal">
				<label className="label">Gender:</label>
			</div>
			<div className="field-body">
				<div className="field is-grouped-centered ">
					<p className="control">
						<span className="select" style={{ width: "100%" }} value={form.gender || genders[0]} onChange={e => setForm('gender', e.target.value)}>
							<select style={{ width: "100%" }}>
								{genders.map((x, key) => <option value={x} key={key}>{x}</option>)}
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
							<select style={{ width: "100%" }} value={form.orientation || orientations[0]} onChange={e => setForm('orientation', e.target.value)}>
								{orientations.map((x, key) => <option value={x} key={key}>{x}</option>)}
							</select>
						</span>
					</p>
				</div>
				<div className="field-label is-normal">
					<label className="label">Age:</label>
				</div>
				<div className="field">
					<div className="control">
						<input className="input" type="date" value={date2Html(form.birthdate) || ""} onChange={e => setForm('birthdate', new Date(e.target.value).valueOf())} />
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
						<textarea className="textarea" placeholder="Explain how we can help you" value={form.bio || ""} onChange={e => setForm('bio', e.target.value)} />
					</div>
				</div>
			</div>
		</div>
	</div>
)

const delet_tag = (form, setForm, index) => { form.tags.splice(index, 1); setForm('tags', form.tags); }

const add_tag = (form, setForm, id) => () => {
	const elem = document.getElementById(id);
	if (!elem.value) return;
	if ((form.tags || []).includes(elem.value)) {
		elem.value = '';
		return;
	}
	setForm('tags', [...(form.tags || []), elem.value]);
	elem.value = '';
}

const Tags = (form, setForm, key) => {
	const input_id = "NEW_TAGS_MF_PRIVATE";

	return (
		<div key={key}>
			<hr className="hr" />
			<div className="field is-horizontal is-grouped-centered">
				<div className="field-label is-normal">
					<label className="label">Tags:</label>
				</div>
				<div className="field-body">
					<div className="field has-addons" style={{ flexGrow: "0", minWidth: "10em" }}>
						<div className="control">
							<input id={input_id} className="input" type="text" placeholder="Enter a tag" />
						</div>
						<div className="control">
							{/*TODO: deplucate tags empty tags */}
							<span className="button is-info" onClick={add_tag(form, setForm, input_id)}>
								OK
							</span>
						</div>
					</div>
					<div className="tags">
						{(form.tags || []).map((tag, key) => (
							<span key={key} className="tag">
								{tag}
								<button className="delete is-small" onClick={() => delet_tag(form, setForm, key)}></button>
							</span>
						))}
					</div>
				</div>
			</div>
		</div>
	)
}

const Photos = (form, setForm, key) => (
	<div key={key} >
		<hr className="hr" />
		<div className="card">
			<div className="card-image">
				<figure className="image">
					<img alt="" src="https://bulma.io/images/placeholders/1280x960.png" />
				</figure>
			</div>
		</div>
		<div className="field">
			<div className="file is-boxed" style={{ justifyContent: "center" }}>
				<label className="file-label">
					<input className="file-input" type="file" name="resume" />
					<span className="file-cta">
						<span className="file-icon">
							<i className="fas fa-cloud-upload-alt"></i>
						</span>
						<span className="file-label">
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

const send_info = async (form, setErrors, setIsLoading, history) => {
	if (!form) return;
	setIsLoading(true)
	form.tags = undefined; // TODO: remove
	form.birthdate = undefined; // TODO: remove
	form.gender = undefined; // TODO: remove
	const res = await apiCall({ uri: "/profile/complete", method: "POST", body: form })
	if (res.is_error) {
		setIsLoading(false);
		setErrors([res.error.message])
	} else {
		localStorage.removeItem("onboarding");
		setIsLoading(false);
		history.push("/");
	}
}

const OnboardingPage = () => {
	const history = useHistory();
	const [page, setPage] = useState(0);
	const [form, setForm] = useState({});
	const [errors, setErrors] = useState([]);
	const [is_loading, setIsLoading] = useState(false);

	if (!getRefreshToken())
		history.push('/login');
	if (localStorage.getItem("onboarding") !== "true")
		history.push('/');

	if (!!is_loading) return <Loading heart_color="red" style={{ position: 'absolute', left: '50%', top: '50%', opacity: '1', marginTop: "50vh" }} />
	return (
		<div>
			<Errors errors={errors} />
			<h1 className="title">On Baording</h1>
			<div className="content">
				<div className="mobile">
					{pages[page](form, inputState(setForm))}
				</div>
				<div className="desktop">
					{pages.map((page, key) => page(form, inputState(setForm), key))}
				</div>
			</div>
			<hr className="hr" />
			<div className="mobile">
				<div style={{ display: "flex", justifyContent: "space-around" }}>
					{!!page &&
						<p className="control" onClick={() => setPage(state => state - (state < 1 ? 0 : 1))}>
							<span className="button is-light">
								Precedent
					</span>
						</p>
					}
					<p className="control" onClick={() => setPage(state => state + (state + 2 > pages.length ? 0 : 1))}>
						<span className="button is-primary">
							Suivant
					</span>
					</p>
				</div>
			</div>
			<div className="desktop">
				<p className="control" style={{ textAlign: "center" }} onClick={() => send_info(verify_entry(form, setErrors), setErrors, setIsLoading, history)}>
					<span className="button is-primary">
						Suivant
					</span>
				</p>
			</div>
		</div>
	)
}

export default OnboardingPage;