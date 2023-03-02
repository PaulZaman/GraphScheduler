function Scheduled({ setScheduled }) {
  return (
    <div>
      <h1>Scheduled</h1>
      <div
        className={`absolute top-64 rounded p-2 w-40 text-center right-10 bg-2 ${
          !content.negativeEdges && !content.containsCycles ? "" : "opacity-50"
        } `}
        onClick={() => setScheduled(false)}
      >
        Back to Tests
      </div>
    </div>
  );
}

export default Scheduled;
