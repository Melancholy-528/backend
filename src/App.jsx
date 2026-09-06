import { useState } from "react";
import Login from "./pages/Login";
import Details from "./pages/Details";
import Chat from "./pages/Chat";
import Banks from "./pages/Banks";

function App() {
  const [page, setPage] = useState("login");

  // Selected scheme ki banking information
  const [selectedBankData, setSelectedBankData] = useState(null);

  if (page === "login") {
    return (
      <Login
        onLogin={() => setPage("details")}
      />
    );
  }

  if (page === "details") {
    return (
      <Details
        onOpenChat={() => setPage("chat")}

        onOpenBanks={(data) => {
          setSelectedBankData(data);
          setPage("banks");
        }}
      />
    );
  }

  if (page === "chat") {
    return <Chat />;
  }

  if (page === "banks") {
    return (
      <Banks
        bankData={selectedBankData}
      />
    );
  }

  return null;
}

export default App;