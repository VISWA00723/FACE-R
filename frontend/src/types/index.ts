/**
 * TypeScript type definitions
 */

export interface Employee {
  id: number;
  employee_id: string;
  name: string;
  department: string;
  image_count: number;
  created_at: string;
  updated_at: string;
}

export interface EmployeeCreate {
  employee_id: string;
  name: string;
  department: string;
  images: string[];
}

export interface AttendanceLog {
  id: number;
  employee_id: string;
  employee_name?: string;
  department?: string;
  log_date: string;
  in_time: string | null;
  out_time: string | null;
  duration: number | null;
  status: string;
  created_at: string;
}

export interface AttendanceTodayResponse {
  date: string;
  total_employees: number;
  present: number;
  absent: number;
  in_count: number;
  out_count: number;
  attendance_logs: AttendanceLog[];
}

export interface AttendanceHistoryResponse {
  total: number;
  attendance_logs: AttendanceLog[];
}

export interface FaceRecognitionResponse {
  recognized: boolean;
  employee_id: string | null;
  name: string | null;
  department: string | null;
  confidence: number | null;
  status: string;
  timestamp: string;
  message: string;
}

export interface AttendanceStats {
  start_date: string;
  end_date: string;
  total_employees: number;
  average_present: number;
  daily_stats: DailyStat[];
}

export interface DailyStat {
  date: string;
  present: number;
  in: number;
  out: number;
}
