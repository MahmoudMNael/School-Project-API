# class AssignmentDetailView(APIView):
# 	def get(self, request, classroom_id, assignment_id):
# 		current_user = is_logged_in(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if current_user.role == 'admin' or classroom.teacher == current_user or current_user in classroom.students.all():
# 			serializer = AssignmentSerializer(assignment)
# 			return Response(serializer.data, status=status.HTTP_200_OK)
# 		else:
# 			raise exceptions.PermissionDenied('You do not have permission to view this assignment')
		
# 	def put(self, request, classroom_id, assignment_id):
# 		current_user = is_teacher(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if classroom.teacher != current_user:
# 			raise exceptions.PermissionDenied('You do not have permission to update this assignment')
		
# 		title = request.data.get('title')
# 		content = request.data.get('content')
# 		due_date = request.data.get('due_date')

# 		try:
# 			assignment.title = title
# 			assignment.content = content
# 			assignment.due_date = due_date
# 			assignment.save()
# 			serializer = AssignmentSerializer(assignment)
# 			return Response(serializer.data, status=status.HTTP_200_OK)
# 		except:
# 			raise exceptions.ValidationError('An error occurred while updating the assignment')
		
# 	def delete(self, request, classroom_id, assignment_id):
# 		current_user = is_teacher(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if classroom.teacher != current_user:
# 			raise exceptions.PermissionDenied('You do not have permission to delete this assignment')
		
# 		assignment.delete()
# 		return Response(status=status.HTTP_200_OK)




# class CommentsListView(APIView):
# 	def get(self, request, classroom_id, assignment_id):
# 		current_user = is_logged_in(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if current_user.role == 'admin' or classroom.teacher == current_user or current_user in classroom.students.all():
# 			comments = assignment.comments.order_by('-created_at').all()
# 			serialized_comments = CommentSerializer(comments, many=True)
# 			return Response(serialized_comments.data, status=status.HTTP_200_OK)
# 		else:
# 			raise exceptions.PermissionDenied('You do not have permission to view the comments for this assignment')
		
# 	def post(self, request, classroom_id, assignment_id):
# 		current_user = is_logged_in(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if current_user.role == 'admin' or classroom.teacher == current_user or current_user in classroom.students.all():
# 			content = request.data.get('content')

# 			try:
# 				comment = Comment(content=content, assignment=assignment, created_by=current_user)
# 				comment.save()
# 				serializer = CommentSerializer(comment)
# 				return Response(serializer.data, status=status.HTTP_201_CREATED)
# 			except:
# 				raise exceptions.ValidationError('An error occurred while creating the comment')
# 		else:
# 			raise exceptions.PermissionDenied('You do not have permission to create a comment for this assignment')

# class CommentActionView(APIView):
# 	def put(self, request, classroom_id, assignment_id, comment_id):
# 		current_user = is_logged_in(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()
# 		comment = Comment.objects.filter(id=comment_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if not comment:
# 			raise exceptions.NotFound('Comment not found')
		
# 		if current_user == comment.created_by:
# 			content = request.data.get('content')
# 			comment.content = content
# 			comment.save()
# 			serializer = CommentSerializer(comment)
# 			return Response(serializer.data, status=status.HTTP_200_OK)
# 		else:
# 			raise exceptions.PermissionDenied('You do not have permission to edit this comment')
	
# 	def delete(self, request, classroom_id, assignment_id, comment_id):
# 		current_user = is_logged_in(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()
# 		comment = Comment.objects.filter(id=comment_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if not comment:
# 			raise exceptions.NotFound('Comment not found')
		
# 		if current_user == comment.created_by:
# 			comment.delete()
# 			return Response(status=status.HTTP_200_OK)
# 		else:
# 			raise exceptions.PermissionDenied('You do not have permission to delete this comment')


# class SubmissionsListView(APIView):
# 	def get(self, request, classroom_id, assignment_id):
# 		current_user = is_logged_in(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if current_user.role == 'admin' or classroom.teacher == current_user:
# 			submissions = assignment.submissions.order_by('-created_at').all()
# 			serialized_submissions = SubmissionSerializer(submissions, many=True)
# 			return Response(serialized_submissions.data, status=status.HTTP_200_OK)
# 		else:
# 			raise exceptions.PermissionDenied('You do not have permission to view the submissions for this assignment')
		
# 	def post(self, request, classroom_id, assignment_id):
# 		current_user = is_logged_in(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if current_user in classroom.students.all():
# 			link = request.data.get('link')

# 			try:
# 				submission = Submission(link=link, assignment=assignment, created_by=current_user)
# 				submission.save()
# 				serializer = SubmissionSerializer(submission)
# 				return Response(serializer.data, status=status.HTTP_201_CREATED)
# 			except:
# 				raise exceptions.ValidationError('An error occurred while creating the submission')
# 		else:
# 			raise exceptions.PermissionDenied('You do not have permission to create a submission for this assignment')


# class SubmissionActionView(APIView):
# 	def put(self, request, classroom_id, assignment_id, submission_id):
# 		current_user = is_logged_in(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()
# 		submission = Submission.objects.filter(id=submission_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if not submission:
# 			raise exceptions.NotFound('Submission not found')
		
# 		if submission.created_by != current_user:
# 			raise exceptions.PermissionDenied('You do not have permission to edit this submission')
		
# 		link = request.data.get('link')
# 		submission.link = link
# 		submission.save()
# 		serializer = SubmissionSerializer(submission)
# 		return Response(serializer.data, status=status.HTTP_200_OK)

# 	def delete(self, request, classroom_id, assignment_id, submission_id):
# 		current_user = is_logged_in(request)
# 		classroom = Classroom.objects.filter(id=classroom_id).first()
# 		assignment = Assignment.objects.filter(id=assignment_id).first()
# 		submission = Submission.objects.filter(id=submission_id).first()

# 		if not classroom:
# 			raise exceptions.NotFound('Classroom not found')
		
# 		if not assignment:
# 			raise exceptions.NotFound('Assignment not found')
		
# 		if not submission:
# 			raise exceptions.NotFound('Submission not found')
		
# 		if classroom.teacher != current_user or submission.created_by != current_user:
# 			raise exceptions.PermissionDenied('You do not have permission to delete this submission')
		
# 		submission.delete()
# 		return Response(status=status.HTTP_200_OK)