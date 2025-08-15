
function ReportVehicle() {
  return (
    <div className="report-vehicle-page">
        <form action="" method="post">
            <h1 className="text-2xl font-bold mb-4">Report a Vehicle</h1>
            <div className="mb-4">
                <label htmlFor="vehicleNo" className="block text-sm font-medium text-gray700">Vehicle No.</label>
                <input type="text" id="vehicleNo" name="vehicleNo" required className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500" />
            </div>
            <div className="mb-4">
                <label htmlFor="vehicleType" className="block text-sm font-medium text-gray-700">Vehicle Type</label>
                <select id="vehicleType" name="vehicleType" required className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500">
                    <option value="">Select a vehicle type</option>
                    <option value="bike">Bike</option>
                    <option value="car">Car</option>
                </select>
            </div>
        </form>
    </div>
  );
}

export default ReportVehicle;