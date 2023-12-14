import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { Amplify } from "aws-amplify";
import { locations } from "../library/constants";
import { getAmplifyConfig } from "../config/getAmplifyConfig";

import LocationSelection from "./LocationSelection";
import Registration from "./Registration";
import SignInSuccess from "./SignInSuccess";
import SignInError from "./SignInError";
import NotFoundPage from "./NotFoundPage";
import VisitForm from "../components/VisitForm";
import Admin from "./Admin";
import Quizzes from "./QuizStatus";

const config = getAmplifyConfig();

Amplify.configure({
  Auth: {
    Cognito: {
      //  Amazon Cognito User Pool ID
      userPoolId: config.userPoolId,
      // Amazon Cognito Web Client ID
      userPoolClientId: config.userPoolClientId,
    },
  },
});

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LocationSelection />} />
        <Route path="/register" element={<Registration />} />
        <Route path="/success" element={<SignInSuccess />} />
        <Route path="/error" element={<SignInError />} />
        <Route path="*" element={<NotFoundPage />} />

        <Route path="/admin" element={<Admin />} />
        <Route path="/quiz_status" element={<Quizzes />} />

        {/* makerspace specific routes */}
        {locations.map((location) => {
          const { slug } = location;
          return (
            <Route
              path={`/${slug}`}
              key={slug}
              element={<VisitForm location={location} />}
            />
          );
        })}
      </Routes>
    </Router>
  );
};

export default App;
